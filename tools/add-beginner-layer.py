#!/usr/bin/env python3
"""Add a short, article-specific orientation section to every CS article.

The existing articles are intentionally deep interview notes. This script keeps
that material intact and adds a predictable on-ramp before section 1 so a
beginner knows the problem, the use case, and the words that matter first.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"assets", "tools", "_template"}

TOPIC_INTRO = {
    "Concurrency": "Nhiều việc cùng chạy trong một chương trình. Khó ở chỗ các việc có thể chạm cùng dữ liệu và làm kết quả sai nếu không phối hợp.",
    "Database": "Nơi ứng dụng lưu dữ liệu và đọc lại dữ liệu. Khó ở chỗ dữ liệu phải đúng khi nhiều người cùng đọc, ghi, hoặc khi máy bị lỗi.",
    "Distributed Systems": "Nhiều máy cùng phục vụ một hệ thống. Khó ở chỗ mạng có thể chậm hoặc đứt, máy có thể hỏng, nhưng người dùng vẫn cần kết quả hợp lý.",
    "Memory - Runtime": "Cách chương trình dùng và thu hồi bộ nhớ khi đang chạy. Hiểu phần này giúp giải thích chậm, treo, crash và out-of-memory.",
    "Networking": "Cách trình duyệt, ứng dụng và máy chủ gửi dữ liệu cho nhau. Mỗi bước có giao thức, độ trễ và kiểu lỗi riêng.",
    "OOP - Design Patterns": "Cách tổ chức code thành những đối tượng dễ thay đổi. Mục tiêu là giữ luật của nghiệp vụ rõ ràng và tránh code phụ thuộc chặt vào nhau.",
    "Operating Systems": "Lớp phần mềm quản lý CPU, bộ nhớ, tiến trình và thiết bị. Ứng dụng gọi OS thay vì tự điều khiển phần cứng trực tiếp.",
}

PLAIN = {
    # Concurrency
    "compare-and-swap": "CAS là thao tác: chỉ ghi giá trị mới nếu giá trị hiện tại vẫn đúng như mình đã đọc. Nó giúp nhiều luồng sửa cùng một biến mà không cần khóa ngay từ đầu.",
    "concurrency-deadlock": "Deadlock là lúc các luồng chờ nhau mãi nên không luồng nào đi tiếp. Bài tập trung vào cách nhận ra vòng chờ và phá vòng đó.",
    "concurrency-vs-parallelism": "Concurrency là quản lý nhiều việc trong cùng khoảng thời gian; parallelism là thật sự chạy nhiều việc cùng lúc trên nhiều lõi CPU.",
    "condition-variable": "Condition variable cho phép một luồng ngủ cho tới khi điều kiện đúng, thay vì liên tục kiểm tra và đốt CPU.",
    "mutex-vs-lock": "Lock là tên chung cho cơ chế bảo vệ dữ liệu; mutex là loại lock chỉ cho một luồng vào vùng quan trọng tại một thời điểm.",
    "race-condition": "Race condition xảy ra khi kết quả phụ thuộc vào việc luồng nào chạy trước. Ví dụ hai luồng cùng tăng một bộ đếm nhưng một lần tăng bị mất.",
    "sync-vs-async-io": "Synchronous I/O khiến luồng chờ kết quả; asynchronous I/O cho phép luồng làm việc khác trong lúc thiết bị hoặc mạng xử lý.",
    "thread-pool": "Thread pool tạo sẵn một nhóm luồng, rồi cho các luồng lấy việc từ hàng đợi. Cách này tránh tạo quá nhiều luồng và giới hạn tải.",
    # Database
    "acid-properties": "ACID là bốn lời hứa của transaction: làm trọn vẹn, giữ dữ liệu hợp lệ, cô lập các giao dịch và không mất dữ liệu đã commit.",
    "b-plus-tree-index": "Index B+ tree là cấu trúc phụ giúp database tìm dòng theo khóa mà không phải đọc toàn bộ bảng.",
    "clustered-vs-non-clustered-index": "Clustered index sắp dữ liệu thật theo khóa; non-clustered index giữ một danh sách khóa rồi trỏ tới dòng. Khác biệt này ảnh hưởng tốc độ đọc và ghi.",
    "connection-pooling": "Connection pool giữ sẵn các kết nối database để request dùng lại, thay vì mở một kết nối mới cho mỗi request.",
    "database-deadlock": "Database deadlock xảy ra khi hai transaction giữ các khóa khác nhau rồi chờ khóa của nhau. Engine phải chọn một transaction để hủy.",
    "database-denormalization": "Denormalization cố ý lặp hoặc gộp dữ liệu để đọc nhanh hơn, đổi lại việc ghi và đồng bộ trở nên khó hơn.",
    "database-isolation-levels": "Isolation level quy định một transaction được nhìn thấy thay đổi của transaction khác tới đâu.",
    "database-normalization": "Normalization chia dữ liệu thành các bảng hợp lý để giảm lặp và tránh sửa một nơi nhưng quên nơi khác.",
    "database-replication": "Replication sao chép dữ liệu sang nhiều database để chịu lỗi và phục vụ nhiều lượt đọc hơn.",
    "database-sharding": "Sharding chia dữ liệu ra nhiều máy theo một khóa, ví dụ user_id, để một máy không phải chứa và xử lý tất cả.",
    "database-transaction": "Transaction gom nhiều câu lệnh thành một công việc: hoặc mọi thay đổi được ghi, hoặc không thay đổi nào được giữ lại.",
    "indexing-for-get-requests": "Thiết kế index tốt bắt đầu từ câu SELECT thật sự chạy, rồi sắp cột trong index theo điều kiện lọc và sắp xếp.",
    "inner-join-vs-left-join": "INNER JOIN chỉ giữ các dòng có cặp ở cả hai bảng; LEFT JOIN giữ toàn bộ dòng bên trái dù bên phải không có cặp.",
    "optimistic-vs-pessimistic-locking": "Pessimistic locking chặn trước khi sửa; optimistic locking cho phép sửa rồi kiểm tra version để phát hiện xung đột.",
    "primary-key-vs-unique-key": "Primary key định danh mỗi dòng và là khóa chính của bảng; unique key chỉ yêu cầu các giá trị không trùng.",
    "rdbms-to-nosql-migration": "Chuyển từ RDBMS sang NoSQL cần vừa sao chép dữ liệu vừa giữ dịch vụ chạy, rồi kiểm chứng trước khi chuyển traffic.",
    "sql-vs-nosql": "SQL dùng bảng và quan hệ rõ ràng; NoSQL có nhiều kiểu dữ liệu khác nhau và thường ưu tiên scale hoặc cách truy cập cụ thể.",
    "two-phase-commit": "2PC giúp nhiều database cùng commit một giao dịch, nhưng coordinator hỏng có thể làm các bên chờ lâu.",
    "write-ahead-log": "WAL ghi mô tả thay đổi vào log trước khi ghi page dữ liệu. Nếu máy crash, database đọc log để phục hồi.",
    # Distributed
    "cap-theorem": "CAP nói rằng khi mạng bị chia cắt, hệ thống phải ưu tiên nhất quán hoặc sẵn sàng phục vụ; không thể đảm bảo cả hai tuyệt đối.",
    "eventual-vs-strong-consistency": "Strong consistency cho kết quả mới nhất ngay; eventual consistency cho phép đọc tạm thời cũ nhưng các bản sao sẽ hội tụ.",
    "idempotency": "Một thao tác idempotent có thể được gửi lại mà không tạo thêm side effect, rất quan trọng khi client retry vì timeout.",
    "keeping-distributed-systems-consistent": "Giữ nhiều service nhất quán cần chọn đúng công cụ: transaction cục bộ, outbox, saga, quorum hoặc consensus.",
    "load-balancer": "Load balancer nhận request rồi chọn một server khỏe để xử lý, nhờ đó tránh dồn tất cả traffic vào một máy.",
    "monolith-vs-microservices": "Monolith triển khai một khối; microservices tách thành nhiều service. Tách service đổi sự đơn giản lấy khả năng triển khai độc lập và chi phí vận hành.",
    # Memory
    "final-finalize-finally": "Trong Java, final là từ khóa, finalize là phương thức cũ, còn finally là khối dọn dẹp. Ba từ giống nhau nhưng có vai trò hoàn toàn khác.",
    "garbage-collection": "Garbage collector tìm object không còn đường nào dùng tới rồi thu hồi bộ nhớ, để lập trình viên không phải free thủ công.",
    "mark-sweep-vs-generational-gc": "Mark-and-sweep quét một vùng nhớ; generational GC chia object theo tuổi để xử lý nhanh nhóm object mới thường chết sớm.",
    "memory-leak": "Memory leak là bộ nhớ vẫn bị giữ dù chương trình không còn cần. Chương trình có thể tăng RAM dần rồi bị hệ điều hành kill.",
    "pass-by-value-vs-reference": "Pass-by-value truyền một bản sao của giá trị; với Java và Python, biến có thể chứa reference nhưng reference đó vẫn được truyền by value.",
    "reference-counting-gc": "Reference counting giữ số lượng reference tới mỗi object và giải phóng ngay khi số này về 0, nhưng cần cách xử lý vòng tham chiếu.",
    "stack-vs-heap": "Stack giữ dữ liệu gắn với lời gọi hàm; heap giữ object sống lâu hoặc có kích thước động. Nhầm hai vùng thường gây stack overflow hoặc out-of-memory.",
    # Networking
    "arp-vs-dns": "DNS tìm IP từ tên miền; ARP tìm địa chỉ MAC của máy kế tiếp trong mạng nội bộ. Một request web thường cần cả hai.",
    "authn-vs-authz": "Authentication trả lời 'bạn là ai'; authorization trả lời 'bạn được phép làm gì'. Đăng nhập thành công chưa có nghĩa là được đọc mọi dữ liệu.",
    "cdn-performance": "CDN đặt bản sao nội dung ở nhiều điểm gần người dùng, giảm quãng đường mạng và giảm tải server gốc.",
    "cookies-vs-sessions": "Cookie nằm trong request phía client; session là trạng thái phía server thường được tìm bằng một session ID trong cookie.",
    "dns-how-it-works": "DNS đổi tên dễ nhớ như api.example.com thành địa chỉ IP để máy biết kết nối tới đâu, rồi cache kết quả theo TTL.",
    "http-status-codes": "HTTP status code là tín hiệu ngắn cho client biết request thành công, chuyển hướng, sai ở client hay lỗi ở server.",
    "http-vs-https": "HTTPS là HTTP chạy trong TLS, giúp xác thực server và mã hóa dữ liệu trên đường truyền.",
    "http1-vs-http2": "HTTP/1.1 gửi các request theo text và dễ bị chờ tuần tự; HTTP/2 dùng frame nhị phân và nhiều stream trên một kết nối.",
    "ip-differences": "IPv4 dùng địa chỉ 32 bit; IPv6 dùng 128 bit và giải quyết tình trạng thiếu địa chỉ IPv4.",
    "nat-how-it-works": "NAT đổi địa chỉ và cổng private thành địa chỉ public khi gói tin đi ra Internet, rồi đổi ngược khi phản hồi quay về.",
    "osi-model": "OSI chia việc truyền dữ liệu thành bảy lớp để dễ thiết kế và debug; mỗi lớp thêm header của mình rồi chuyển xuống lớp dưới.",
    "rest-api-principles": "REST tổ chức API quanh resource, HTTP method và representation; stateless nghĩa là mỗi request tự mang đủ thông tin cần thiết.",
    "tcp-three-way-handshake": "TCP bắt tay bằng SYN, SYN-ACK, ACK để hai phía biết kết nối tồn tại và đồng bộ số thứ tự trước khi gửi byte dữ liệu.",
    "tcp-vs-udp": "TCP đảm bảo byte stream đúng thứ tự; UDP gửi từng datagram với ít cơ chế bảo đảm hơn để đổi lấy độ trễ và quyền kiểm soát.",
    "tls-ssl-how-it-works": "TLS thương lượng khóa rồi mã hóa từng record, đồng thời dùng certificate để client kiểm tra mình đang nói chuyện với đúng server.",
    "type-google-com-in-browser": "Một lần gõ URL đi qua parse, DNS, kết nối TCP hoặc QUIC, TLS, HTTP, server, trình duyệt và nhiều lớp cache.",
    "when-to-use-udp": "Dùng UDP khi dữ liệu mới quan trọng hơn dữ liệu cũ hoặc ứng dụng tự xử lý retry, thứ tự và mất gói.",
    # OOP
    "abstraction-in-oop": "Abstraction cho người dùng một contract đơn giản và giấu cách bên trong thực hiện contract đó.",
    "adapter-pattern": "Adapter bọc một interface cũ để nó nói chuyện được với code đang mong đợi interface mới.",
    "encapsulation-in-oop": "Encapsulation giữ state và hành vi trong một object, chỉ cho bên ngoài thay đổi qua các method bảo vệ luật dữ liệu.",
    "factory-pattern": "Factory gom quyết định tạo object vào một chỗ, để code gọi không phải biết class cụ thể nào sẽ được tạo.",
    "inheritance-and-composition": "Inheritance biểu diễn quan hệ is-a; composition ghép các object nhỏ thành object lớn và thường dễ thay đổi hơn.",
    "interface-vs-abstract-class": "Interface chủ yếu mô tả contract; abstract class có thể chia sẻ state và code chung cho các class con.",
    "observer-pattern": "Observer cho phép một subject báo cho nhiều listener khi state thay đổi mà subject không cần biết chi tiết listener làm gì.",
    "polymorphism": "Polymorphism cho phép cùng một lời gọi method nhưng object thật có thể chọn cách thực hiện khác nhau.",
    "singleton-pattern": "Singleton giới hạn một class còn một instance trong một process, nhưng global state khiến code khó test và khó scale.",
    "strategy-pattern": "Strategy tách các cách xử lý khác nhau thành các object thay thế được, thay vì một if-else dài.",
    # OS
    "context-switching": "Context switch lưu trạng thái của việc đang chạy rồi nạp trạng thái việc khác, giúp CPU chia thời gian giữa các task.",
    "cpu-scheduling": "CPU scheduling quyết định task nào được chạy tiếp. Mỗi chính sách cân bằng khác nhau giữa độ phản hồi, công bằng và throughput.",
    "dining-philosophers-problem": "Bài toán dining philosophers mô phỏng nhiều task cùng cần tài nguyên, cho thấy deadlock và starvation có thể xuất hiện thế nào.",
    "interrupt-handling": "Interrupt tạm dừng luồng CPU hiện tại để báo một sự kiện như packet đến hoặc timer hết hạn, rồi kernel xử lý sự kiện đó.",
    "mutex-vs-semaphore": "Mutex bảo vệ một vùng dữ liệu và có owner; semaphore là bộ đếm quyền, phù hợp để giới hạn số task dùng tài nguyên.",
    "os-deadlock": "OS deadlock là vòng chờ tài nguyên giữa các process hoặc thread. Muốn xử lý cần phòng, tránh, phát hiện hoặc phục hồi.",
    "paging-vs-segmentation": "Paging chia bộ nhớ thành page kích thước cố định; segmentation chia theo vùng có ý nghĩa như code, stack hoặc data.",
    "priority-inversion": "Priority inversion xảy ra khi task ưu tiên cao phải chờ task ưu tiên thấp, trong khi task trung gian liên tục chiếm CPU.",
    "process-vs-thread": "Process có không gian địa chỉ riêng; thread là luồng chạy bên trong process và thường chia sẻ bộ nhớ với các thread cùng process.",
    "system-call-and-kernel-mode": "System call là cổng để code user yêu cầu kernel làm việc đặc quyền như đọc file hoặc tạo process.",
    "tlb": "TLB là cache nhỏ trong MMU, lưu ánh xạ từ địa chỉ ảo sang địa chỉ vật lý để CPU không phải đọc page table mỗi lần.",
    "virtual-memory": "Virtual memory cho mỗi process một không gian địa chỉ riêng và chỉ nạp page cần thiết vào RAM, giúp bảo vệ và dùng RAM hiệu quả hơn.",
}

SCENARIO = {
    "compare-and-swap": "Hai request cùng cập nhật số lượng tồn kho từ 10 xuống 9. CAS giúp chỉ một request ghi thành công trên phiên bản mà nó đã đọc.",
    "concurrency-deadlock": "Thread A giữ khóa đơn hàng rồi chờ khóa kho; thread B giữ khóa kho rồi chờ khóa đơn hàng. Cả hai đứng im vì chờ vòng tròn.",
    "concurrency-vs-parallelism": "Một server nhận request và xen kẽ xử lý chúng là concurrency; hai lõi xử lý hai request thật sự cùng lúc là parallelism.",
    "condition-variable": "Worker ngủ khi hàng đợi rỗng và được đánh thức khi producer thêm việc, thay vì kiểm tra hàng đợi liên tục.",
    "mutex-vs-lock": "Hai request cùng sửa số dư tài khoản cần một mutex để chỉ một request đọc-sửa-ghi tại một thời điểm.",
    "race-condition": "Hai người cùng bấm mua món cuối cùng. Nếu không đồng bộ, cả hai có thể được báo mua thành công dù kho chỉ còn một.",
    "sync-vs-async-io": "Trong lúc chờ database trả kết quả, server async có thể xử lý request khác; server sync giữ thread chờ ở lệnh đọc.",
    "thread-pool": "API nhận 10.000 request nhưng chỉ cho 100 task gọi database cùng lúc bằng pool và queue có giới hạn.",
    "acid-properties": "Chuyển tiền phải trừ A và cộng B cùng nhau; database không được giữ trạng thái chỉ trừ A sau khi máy crash.",
    "b-plus-tree-index": "Tìm đơn hàng theo order_id bằng index đi qua vài node thay vì quét hàng triệu dòng.",
    "clustered-vs-non-clustered-index": "Đọc các đơn hàng liên tiếp theo user_id nhanh hơn khi dòng dữ liệu nằm gần nhau theo đúng khóa clustered.",
    "connection-pooling": "Mỗi request dùng một connection có sẵn, trả lại pool sau khi xong; request không phải bắt tay TCP và xác thực database lại.",
    "database-deadlock": "Transaction thanh toán khóa account trước, transaction hoàn tiền khóa payment trước; thứ tự đảo nhau tạo vòng chờ.",
    "database-denormalization": "Trang danh sách đơn đọc nhanh hơn nếu lưu sẵn customer_name, nhưng đổi tên khách hàng phải cập nhật nhiều dòng.",
    "database-isolation-levels": "Một transaction đọc số dư trong khi transaction khác đang cập nhật; isolation level quyết định nó thấy số cũ, số mới hay phải chờ.",
    "database-normalization": "Thông tin khách hàng chỉ lưu một lần, bảng order giữ customer_id; sửa email không cần sửa hàng nghìn order.",
    "database-replication": "Primary nhận lệnh ghi và replica phục vụ đọc; nếu replica trễ, người dùng vừa đặt hàng có thể chưa thấy đơn ngay.",
    "database-sharding": "Đơn của user 42 luôn vào shard theo user_id, nên nhiều máy có thể nhận traffic mà không tranh cùng một bảng.",
    "database-transaction": "Tạo order, trừ tồn kho và ghi payment log cần commit cùng nhau hoặc rollback cùng nhau.",
    "indexing-for-get-requests": "Với GET /orders?user_id=42&status=paid ORDER BY created_at, index nên bắt đầu bằng user_id và status rồi mới tới created_at.",
    "inner-join-vs-left-join": "Báo cáo chỉ khách đã thanh toán dùng INNER JOIN; danh sách mọi khách, kể cả chưa có payment, dùng LEFT JOIN.",
    "optimistic-vs-pessimistic-locking": "Hai nhân viên sửa cùng một hồ sơ; optimistic locking phát hiện version đổi và yêu cầu người đến sau tải lại.",
    "primary-key-vs-unique-key": "user_id là định danh dòng; email có unique constraint để không hai tài khoản dùng cùng email.",
    "rdbms-to-nosql-migration": "Hệ thống cũ vẫn nhận order trong lúc backfill sang store mới; CDC giúp chuyển tiếp các thay đổi mới.",
    "sql-vs-nosql": "Báo cáo nhiều JOIN hợp với SQL; session theo user_id với schema đơn giản có thể hợp với key-value store.",
    "two-phase-commit": "Một order cần ghi cả database order và database payment; coordinator phải biết cả hai đã prepare trước khi commit.",
    "write-ahead-log": "Server crash ngay sau khi trả COMMIT; WAL cho phép database dựng lại thay đổi chưa kịp ghi vào data file.",
    "cap-theorem": "Khi hai datacenter mất liên lạc, hệ thống phải chọn trả lỗi để giữ dữ liệu đúng hoặc tiếp tục nhận ghi rồi hòa giải sau.",
    "eventual-vs-strong-consistency": "Sau khi đổi avatar, một edge cache có thể còn ảnh cũ vài giây nếu hệ thống dùng eventual consistency.",
    "idempotency": "Client timeout sau khi charge thẻ và gửi lại request; idempotency key giúp server không charge lần hai.",
    "keeping-distributed-systems-consistent": "Order service commit thành công nhưng message gửi kho thất bại; outbox giữ message để worker gửi lại.",
    "load-balancer": "Một server lỗi health check sẽ bị loại khỏi pool, request mới chuyển sang server khỏe.",
    "monolith-vs-microservices": "Team nhỏ có thể deploy monolith đơn giản; khi checkout và catalog cần scale độc lập, microservices có thể phù hợp hơn.",
    "final-finalize-finally": "finally chạy để đóng file dù try có lỗi; final ngăn biến hoặc class thay đổi; finalize không phải cách cleanup đáng tin.",
    "garbage-collection": "Request tạo nhiều object tạm; GC dọn object không còn reachable để heap không đầy mãi.",
    "mark-sweep-vs-generational-gc": "Object của request thường chết nhanh nên minor GC chỉ cần quét young generation thay vì quét toàn heap.",
    "memory-leak": "Cache giữ mãi key của user cũ dù không request nào dùng; RSS tăng dần qua nhiều giờ.",
    "pass-by-value-vs-reference": "Hàm nhận một List và thêm phần tử có thể làm list gốc đổi, nhưng gán biến parameter sang list mới không đổi biến caller.",
    "reference-counting-gc": "Hai object trỏ vòng vào nhau nên mỗi refcount vẫn là 1 dù chương trình không thể truy cập chúng nữa.",
    "stack-vs-heap": "Mỗi lần gọi hàm tạo frame trên stack; object đơn hàng cần sống sau khi hàm trả về thường nằm trên heap.",
    "arp-vs-dns": "DNS tìm IP của api.example.com; sau đó ARP tìm MAC của gateway để gói IP rời khỏi laptop.",
    "authn-vs-authz": "Đăng nhập xác minh user là Alice; authorization mới quyết định Alice có được refund order của Bob hay không.",
    "cdn-performance": "Ảnh sản phẩm được trả từ edge gần người mua thay vì đi xuyên về origin ở một khu vực khác.",
    "cookies-vs-sessions": "Browser gửi session_id trong cookie; server dùng ID đó tìm giỏ hàng trong session store.",
    "dns-how-it-works": "Browser hỏi recursive resolver, resolver tra cache hoặc hỏi root, TLD và authoritative để lấy IP.",
    "http-status-codes": "API trả 201 khi tạo order, 401 khi thiếu đăng nhập, 429 khi user vượt rate limit và 503 khi service tạm quá tải.",
    "http-vs-https": "HTTPS ngăn người trên Wi-Fi đọc token và giúp browser biết certificate thuộc đúng tên miền.",
    "http1-vs-http2": "Trang có nhiều ảnh dùng nhiều stream HTTP/2 trên một TCP connection thay vì mở nhiều connection HTTP/1.1.",
    "ip-differences": "IPv4 có thể cần NAT vì thiếu địa chỉ; IPv6 cho mỗi thiết bị không gian địa chỉ lớn hơn nhiều.",
    "nat-how-it-works": "Laptop 192.168.1.10:5000 được router đổi thành public_ip:62000 khi gọi API Internet.",
    "osi-model": "Khi gửi HTTP, ứng dụng tạo request, TCP chia stream, IP định tuyến packet, Ethernet gửi frame qua dây.",
    "rest-api-principles": "GET /orders/42 lấy resource; PUT cùng body gửi lại nhiều lần vẫn nên cho cùng trạng thái cuối.",
    "tcp-three-way-handshake": "Client gửi SYN, server trả SYN-ACK, client ACK rồi mới gửi request HTTP qua connection đã mở.",
    "tcp-vs-udp": "Thanh toán cần TCP để đủ và đúng thứ tự; game state có thể dùng UDP vì frame cũ hết giá trị khi frame mới tới.",
    "tls-ssl-how-it-works": "Client kiểm tra certificate, hai bên dùng ECDHE tạo secret rồi mã hóa request bằng khóa phiên.",
    "type-google-com-in-browser": "Browser tra DNS, tìm route, mở connection, tải HTML rồi tiếp tục tải CSS, JavaScript và ảnh.",
    "when-to-use-udp": "Voice call ưu tiên âm thanh hiện tại hơn việc chờ một packet cũ, nên có thể bỏ packet mất thay vì retransmit.",
    "abstraction-in-oop": "Code gọi paymentGateway.charge() mà không cần biết bên trong dùng HTTP, retry hay ký request.",
    "adapter-pattern": "Code mới cần PaymentGateway nhưng SDK cũ có LegacyBankClient; adapter đổi tên và định dạng method giữa hai bên.",
    "encapsulation-in-oop": "Account không cho đặt balance âm trực tiếp; mọi thay đổi đi qua deposit hoặc withdraw có kiểm tra.",
    "factory-pattern": "Ứng dụng chọn Stripe hoặc PayPal theo config, còn client chỉ gọi factory.createGateway().",
    "inheritance-and-composition": "Bird có thể kế thừa Animal, nhưng ghép Order với PaymentPolicy thường linh hoạt hơn việc tạo quá nhiều subclass.",
    "interface-vs-abstract-class": "Nhiều payment provider cùng implement interface; một abstract class phù hợp khi chúng thật sự chia sẻ state và flow chung.",
    "observer-pattern": "OrderCreated phát cho email, analytics và warehouse listener mà OrderService không gọi cứng từng dependency.",
    "polymorphism": "Danh sách PaymentMethod có thể chứa CardPayment và BankTransfer; cùng gọi pay() nhưng mỗi object xử lý khác.",
    "singleton-pattern": "Một config loader dùng chung có thể là singleton, nhưng global mutable state khiến test và nhiều tenant khó cô lập.",
    "strategy-pattern": "ShippingService chọn StandardShipping hoặc ExpressShipping qua cùng interface thay vì một switch lớn.",
    "context-switching": "CPU lưu thanh ghi của request A rồi nạp thanh ghi của request B để B tiếp tục đúng chỗ đã dừng.",
    "cpu-scheduling": "Round-robin chia mỗi process một time slice; FCFS để process đến trước chạy trước nhưng process dài có thể làm request ngắn chờ.",
    "dining-philosophers-problem": "Năm worker cần hai resource; nếu mỗi worker giữ một resource rồi chờ resource kia, cả nhóm có thể deadlock.",
    "interrupt-handling": "Card mạng báo packet đến bằng interrupt; kernel xử lý phần gấp rồi đưa việc nặng sang bottom half.",
    "mutex-vs-semaphore": "Mutex bảo vệ một cấu trúc; semaphore đếm số connection database còn trống để nhiều worker dùng đồng thời.",
    "os-deadlock": "Hai process giữ file lock chéo nhau; OS cần timeout, thứ tự lock hoặc phát hiện vòng chờ để giải quyết.",
    "paging-vs-segmentation": "Virtual address được tách thành page number và offset; segmentation hợp với các vùng code, data, stack có kích thước khác nhau.",
    "priority-inversion": "UI task ưu tiên cao chờ mutex của task nền, nhưng task trung gian chiếm CPU khiến task nền không chạy để nhả mutex.",
    "process-vs-thread": "Process cô lập crash và bộ nhớ; thread nhẹ hơn và chia sẻ dữ liệu nhanh nhưng một lỗi nghiêm trọng có thể làm cả process chết.",
    "system-call-and-kernel-mode": "read() chuyển từ user mode vào kernel để kiểm tra quyền và lấy byte từ file descriptor.",
    "tlb": "CPU truy cập cùng một mảng nhiều lần và TLB hit giúp bỏ qua bước đọc page table lặp lại.",
    "virtual-memory": "Mỗi process thấy địa chỉ ảo riêng; page chưa có trong RAM gây page fault để OS nạp từ disk hoặc cấp frame mới.",
}

def slug_for(path: Path) -> str:
    return path.stem

def intro(path: Path, title: str, lead: str) -> str:
    topic = path.parent.name
    slug = slug_for(path)
    plain = PLAIN.get(slug, lead.rstrip("."))
    scenario = SCENARIO.get(slug, "Hãy thử liên hệ khái niệm này với một API đặt hàng: request có thể đến đồng thời, dữ liệu có thể lớn, và hệ thống vẫn phải trả lời đúng.")
    keywords = {
        "Concurrency": "thread = luồng chạy; shared state = dữ liệu dùng chung; synchronization = cách phối hợp luồng.",
        "Database": "row = một dòng dữ liệu; query = câu hỏi gửi database; transaction = một nhóm thay đổi được xử lý cùng nhau.",
        "Distributed Systems": "node = một máy hoặc tiến trình; network failure = mạng chậm/đứt; consistency = các nơi nhìn dữ liệu giống nhau tới mức nào.",
        "Memory - Runtime": "object = dữ liệu đang sống; reference = đường trỏ tới object; runtime = phần thực thi chương trình.",
        "Networking": "client = bên gửi request; server = bên phục vụ; packet = mảnh dữ liệu đi qua mạng.",
        "OOP - Design Patterns": "class = khuôn; object = instance cụ thể; method = hành vi mà object cung cấp.",
        "Operating Systems": "process = chương trình đang chạy; thread = luồng thực thi; kernel = phần lõi có quyền điều khiển máy.",
    }[topic]
    return f'''## 0. Nền tảng trước khi đọc

**Bối cảnh:** {TOPIC_INTRO.get(topic, "Bài này giải thích một khái niệm nền tảng trong phát triển phần mềm.")} 

**Nói đơn giản:** {plain}

**Từ khóa cần biết:** {keywords}

**Ví dụ dễ hình dung:** {scenario}

Khi đọc, luôn hỏi ba câu: nó giải quyết vấn đề gì, nó làm việc theo những bước nào, và khi nào không nên dùng?

**Cách học bài này:** Đọc phần này trước để nắm từ khóa; đọc phần 1 để lấy câu trả lời 30 giây; đọc phần 2 để hiểu cơ chế; cuối cùng mở từng câu hỏi ở phần 3 để luyện nói. Các con số và lệnh trong bài là bằng chứng cho câu trả lời, không cần học thuộc nếu chưa hiểu cơ chế.

'''

def main():
    changed = 0
    for path in sorted(ROOT.glob("*/*.md")):
        if path.parent.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        date_index = next((i for i, line in enumerate(lines) if line.startswith("Chủ đề:")), None)
        if date_index is None:
            raise SystemExit(f"Không tìm thấy dòng Chủ đề trong {path}")
        title = next((line[2:].strip() for line in lines if line.startswith("# ")), path.stem)
        lead = next((line[2:].strip() for line in lines if line.startswith("> ")), "")
        beginner_heading = "## 0. Nền tảng trước khi đọc"
        section_one = "## 1. Là gì"
        if beginner_heading in text and section_one in text:
            before, rest = text.split(beginner_heading, 1)
            _, after = rest.split(section_one, 1)
            text = before.rstrip() + "\n\n" + intro(path, title, lead) + section_one + after
            path.write_text(text, encoding="utf-8")
            changed += 1
            continue
        lines.insert(date_index + 1, "\n" + intro(path, title, lead))
        path.write_text("".join(lines), encoding="utf-8")
        changed += 1
    print(f"added beginner layer to {changed} article(s)")

if __name__ == "__main__":
    main()
