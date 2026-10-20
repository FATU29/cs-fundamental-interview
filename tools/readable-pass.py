#!/usr/bin/env python3
"""Give every article the same easy-to-follow interview opening.

The deep interview notes stay below this layer. The added block is intentionally
short and follows the flow used by the browser article: say the idea, walk the
system in a few steps, then point the reader to the deep dive.
"""
from pathlib import Path
import re
import runpy

ROOT = Path(__file__).resolve().parents[1]
data = runpy.run_path(str(ROOT / "tools" / "add-beginner-layer.py"))
PLAIN = data["PLAIN"]
SCENARIO = data["SCENARIO"]

FLOWS = {
    "Concurrency": [
        "Có nhiều task cùng chạy.",
        "Các task chạm vào dữ liệu hoặc tài nguyên chung.",
        "Chương trình dùng message passing, atomic hoặc lock để phối hợp.",
        "Task tiếp tục và kết quả không bị mất, trùng hoặc kẹt.",
    ],
    "Database": [
        "Ứng dụng gửi query qua driver hoặc connection pool.",
        "Database engine tìm dữ liệu, kiểm tra constraint và xử lý transaction.",
        "Engine dùng index, lock/MVCC và log tùy loại thao tác.",
        "Kết quả được trả về; thay đổi chỉ bền vững sau COMMIT.",
    ],
    "Distributed Systems": [
        "Client gửi request tới một node hoặc gateway.",
        "Node gọi các node khác qua mạng và có thể gặp timeout hoặc retry.",
        "Hệ thống chọn cách giữ trạng thái đồng bộ và xử lý lỗi.",
        "Client nhận kết quả hoặc lỗi có thể retry an toàn.",
    ],
    "Memory - Runtime": [
        "Code tạo object hoặc vùng nhớ.",
        "Runtime giữ object còn được dùng và cung cấp reference cho code.",
        "Object không còn reachable sẽ được free hoặc garbage collector thu hồi.",
        "Nếu giữ nhầm, vùng nhớ phình lên và chương trình chậm hoặc hết RAM.",
    ],
    "Networking": [
        "Ứng dụng tạo request với tên host, port và dữ liệu.",
        "OS và các giao thức mạng tìm đường rồi chuyển packet tới server.",
        "Server xử lý request và trả response qua kết nối phù hợp.",
        "Client kiểm tra response, cache hoặc render dữ liệu cho người dùng.",
    ],
    "OOP - Design Patterns": [
        "Client gọi một contract dễ hiểu.",
        "Object hoặc pattern chọn code thực hiện phía sau contract.",
        "State và dependency được giữ ở nơi có trách nhiệm rõ ràng.",
        "Khi requirement đổi, thay implementation mà giảm ảnh hưởng tới client.",
    ],
    "Operating Systems": [
        "Ứng dụng chạy ở user mode và yêu cầu OS khi cần quyền đặc biệt.",
        "Kernel kiểm tra quyền, giữ state và chọn tài nguyên phần cứng.",
        "CPU, memory hoặc device thực hiện công việc; có thể phát sinh interrupt.",
        "Kernel trả kết quả hoặc đánh thức task đang chờ.",
    ],
}

FLOW_OVERRIDES = {
    "type-google-com-in-browser": [
        "Browser parse `google.com`, chọn HTTPS và kiểm tra HSTS/cache.",
        "DNS đổi tên miền thành IP; OS chọn route và tìm MAC của gateway nếu cần.",
        "Browser mở TCP + TLS, hoặc QUIC nếu dùng HTTP/3, rồi gửi HTTP GET.",
        "Google trả HTML; browser parse DOM/CSS, tải resource, layout và vẽ pixel.",
    ],
    # Operating Systems: the shared topic flow is too broad for these concepts.
    "process-vs-thread": [
        "OS tạo một process với address space và tài nguyên riêng.",
        "Process tạo thread; các thread cùng process chia sẻ memory nhưng có stack và register riêng.",
        "Scheduler chọn thread nào chạy trên CPU.",
        "Process cô lập lỗi tốt hơn; thread nhẹ hơn nhưng phải đồng bộ shared state.",
    ],
    "context-switching": [
        "Scheduler quyết định task hiện tại phải nhường CPU.",
        "Kernel lưu register, program counter và state của task đó.",
        "Kernel nạp state của task tiếp theo và có thể đổi address space.",
        "CPU chạy tiếp task mới; chi phí là thời gian lưu/nạp và cache/TLB bị ảnh hưởng.",
    ],
    "cpu-scheduling": [
        "Ready queue chứa các process/thread đang chờ CPU.",
        "Scheduler chọn task theo chính sách như FCFS hoặc Round-Robin.",
        "Task chạy đến khi xong, block I/O hoặc hết time slice.",
        "Scheduler chọn task kế tiếp và cân bằng response time, throughput, fairness.",
    ],
    "virtual-memory": [
        "Process dùng virtual address thay vì địa chỉ RAM trực tiếp.",
        "MMU tra TLB hoặc page table để map virtual page sang physical frame.",
        "Nếu page chưa có trong RAM, CPU tạo page fault để kernel xử lý.",
        "Kernel nạp hoặc tạo page, cập nhật mapping rồi cho instruction chạy lại.",
    ],
    "paging-vs-segmentation": [
        "OS chia address space thành page cố định hoặc segment theo vùng logic.",
        "CPU tách địa chỉ thành phần cần tra và offset.",
        "MMU dùng page table hoặc segment table để kiểm tra quyền và tìm địa chỉ thật.",
        "Thiết kế được chọn dựa trên fragmentation, protection và hardware support.",
    ],
    "tlb": [
        "CPU cần dịch virtual address sang physical address.",
        "MMU kiểm tra TLB trước vì đây là cache của các mapping gần đây.",
        "TLB hit trả frame nhanh; TLB miss buộc MMU hoặc kernel đi đọc page table.",
        "Mapping mới được đưa vào TLB; multiprocessor có thể cần TLB shootdown khi mapping đổi.",
    ],
    "system-call-and-kernel-mode": [
        "Code user gọi wrapper như read(), open() hoặc fork().",
        "CPU đổi từ user mode sang kernel mode qua trap/syscall instruction.",
        "Kernel kiểm tra pointer, quyền và thực hiện thao tác với tài nguyên.",
        "Kernel ghi kết quả hoặc error code rồi trả CPU về user mode.",
    ],
    "interrupt-handling": [
        "Thiết bị hoặc timer phát tín hiệu interrupt tới CPU.",
        "CPU lưu context tối thiểu và nhảy vào handler của kernel.",
        "Handler xử lý phần gấp rồi dời việc nặng sang bottom half/workqueue.",
        "Kernel đánh thức task chờ dữ liệu và khôi phục việc bị ngắt.",
    ],
    "mutex-vs-semaphore": [
        "Thread muốn vào vùng dữ liệu chung hoặc lấy một slot tài nguyên.",
        "Mutex cho một owner vào; semaphore giảm counter nếu còn slot.",
        "Nếu không được cấp, thread ngủ hoặc spin tùy primitive.",
        "Khi owner nhả mutex hoặc counter tăng, một thread chờ được đánh thức.",
    ],
    "os-deadlock": [
        "Thread giữ một tài nguyên và xin thêm tài nguyên khác.",
        "Thread khác giữ tài nguyên kia và chờ tài nguyên đầu tiên.",
        "Wait-for graph tạo chu trình nên không thread nào tiến được.",
        "Hệ thống phá chu trình bằng thứ tự lock, timeout, prevention hoặc recovery.",
    ],
    "priority-inversion": [
        "Task ưu tiên thấp giữ mutex.",
        "Task ưu tiên cao cần mutex nên bị block.",
        "Task ưu tiên trung bình chiếm CPU, làm task thấp không chạy để nhả mutex.",
        "Priority inheritance hoặc priority ceiling nâng task thấp để giải phóng mutex.",
    ],
    "dining-philosophers-problem": [
        "Mỗi worker cần hai resource để làm việc.",
        "Mỗi worker lấy resource thứ nhất rồi chờ resource thứ hai.",
        "Nếu tất cả cùng làm vậy, tạo vòng chờ và deadlock.",
        "Đổi thứ tự lấy resource, giới hạn worker hoặc dùng trylock để phá vòng.",
    ],
    # Database: keep the entry-level flow close to the actual operation.
    "inner-join-vs-left-join": [
        "SQL chọn bảng trái và bảng phải.",
        "Engine so sánh các cột join theo điều kiện ON.",
        "INNER JOIN bỏ dòng không có cặp; LEFT JOIN giữ dòng trái và điền NULL bên phải.",
        "WHERE, index và số dòng quyết định kết quả và chi phí query.",
    ],
    "b-plus-tree-index": [
        "Database nhận điều kiện tìm theo một hoặc nhiều key.",
        "Engine đi từ root qua các internal node của B+ tree.",
        "Leaf node tìm key và row pointer/primary key tương ứng.",
        "Engine đọc row cần thiết thay vì quét toàn bộ bảng.",
    ],
    "indexing-for-get-requests": [
        "Bắt đầu từ câu GET và điều kiện WHERE/ORDER BY thật.",
        "Chọn thứ tự cột index theo equality, range rồi sort phù hợp.",
        "Query planner quyết định dùng index hay full scan.",
        "Đo EXPLAIN và latency trước/sau để tránh index làm write chậm hơn.",
    ],
    "database-normalization": [
        "Tách dữ liệu lặp thành các bảng có ý nghĩa.",
        "Dùng key để liên kết bảng thay vì chép cùng một giá trị nhiều nơi.",
        "Constraint giữ quan hệ và ngăn dữ liệu mâu thuẫn.",
        "Khi đọc cần JOIN; khi cần tốc độ có thể denormalize có chủ đích.",
    ],
    "database-replication": [
        "Primary nhận write và tạo log thay đổi.",
        "Replica đọc log rồi áp dụng lại thay đổi.",
        "Read traffic có thể chuyển tới replica nhưng phải tính replication lag.",
        "Khi primary lỗi, hệ thống chọn replica đủ mới để failover.",
    ],
    "database-sharding": [
        "Ứng dụng chọn shard key từ request.",
        "Router/hash/range map key tới một shard.",
        "Shard xử lý query cục bộ; query không có key có thể fan-out nhiều shard.",
        "Rebalance và hot shard được theo dõi khi dữ liệu hoặc traffic tăng.",
    ],
    "connection-pooling": [
        "Request xin một connection rảnh từ pool.",
        "Pool tạo mới hoặc chờ nếu đã chạm giới hạn.",
        "Request dùng connection để query trong thời gian ngắn.",
        "Sau khi xong, connection được reset và trả về pool cho request khác.",
    ],
    "database-isolation-levels": [
        "Transaction A và B cùng đọc hoặc sửa một vùng dữ liệu.",
        "Engine dùng snapshot, lock hoặc cả hai để quyết định visibility.",
        "Isolation level ngăn dirty read, non-repeatable read và phantom ở mức khác nhau.",
        "Level càng mạnh càng giảm anomaly nhưng có thể tăng wait, abort và contention.",
    ],
}

def mechanism(path: Path, text: str) -> str:
    part = text.split("## 2. Cơ chế cốt lõi", 1)[-1]
    match = re.search(r"^### (.+)$", part, re.M)
    return match.group(1).strip() if match else "các bước cơ chế cốt lõi"

def block(path: Path, text: str) -> str:
    topic = path.parent.name
    slug = path.stem
    plain = PLAIN.get(slug, "Khái niệm này giải quyết một vấn đề thường gặp trong hệ thống phần mềm.")
    scenario = SCENARIO.get(slug, "Hãy liên hệ với một API đặt hàng: request có thể đến đồng thời và hệ thống vẫn phải trả lời đúng.")
    steps = FLOW_OVERRIDES.get(slug, FLOWS[topic])
    mech = mechanism(path, text)
    numbered = "\n".join(f"{i}. {step}" for i, step in enumerate(steps, 1))
    return f'''### Đọc nhanh trước khi đi sâu

**Ý chính:** {plain}

**Ví dụ interview:** {scenario}

**Luồng 4 bước:**

{numbered}

**Nói như trong interview:** {plain} Hãy nói theo bốn bước trên trước; nếu interviewer hỏi sâu, chuyển sang cơ chế **{mech}**, rồi nêu trade-off và failure mode ở các phần sau.

'''

def main():
    changed = 0
    for path in sorted(ROOT.glob("*/*.md")):
        if path.parent.name in {"assets", "tools", "_template"}:
            continue
        text = path.read_text(encoding="utf-8")
        marker = "## 1. Là gì"
        if marker not in text:
            raise SystemExit(f"Không tìm thấy phần 1 trong {path}")
        heading = "### Đọc nhanh trước khi đi sâu"
        if heading in text:
            start = text.index(heading)
            end = text.find("\n## 2. ", start)
            if end == -1:
                end = text.find("\n### ", start + len(heading))
            text = text[:start] + block(path, text).rstrip() + "\n\n" + text[end + 1:]
        else:
            text = text.replace(marker + "\n\n", marker + "\n\n" + block(path, text), 1)
        path.write_text(text, encoding="utf-8")
        changed += 1
    print(f"added readable interview opening to {changed} article(s)")

if __name__ == "__main__":
    main()
