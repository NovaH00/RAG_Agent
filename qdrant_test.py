from qdrant.client import qdrant_service


docs = """Du lịch Việt Nam - Khám phá vẻ đẹp đất nước hình chữ S

Việt Nam là một đất nước có hình dạng độc đáo như chữ S, trải dài từ Bắc vào Nam với bờ biển dài hơn 3.000 km và vô số điểm du lịch hấp dẫn. Từ những dãy núi hùng vĩ ở phía Bắc đến những bãi biển tuyệt đẹp ở miền Nam, Việt Nam mang đến cho du khách những trải nghiệm không thể quên.

Miền Bắc Việt Nam - Nơi lưu giữ nét đẹp truyền thống

Hà Nội - thủ đô ngàn năm văn hiến của Việt Nam, là nơi khởi đầu lý tưởng cho chuyến du lịch khám phá miền Bắc. Phố cổ Hà Nội với những con phố nhỏ hẹp, kiến trúc Pháp cổ kính và không khí náo nhiệt của cuộc sống đô thị tạo nên một bức tranh sinh động. Du khách có thể thưởng thức các món ăn đường phố nổi tiếng như phở, bún chả, bánh mì và cà phê vỉa hè đặc trưng.

Vịnh Hạ Long, một trong bảy kỳ quan thiên nhiên thế giới, là điểm đến không thể bỏ qua khi đến miền Bắc. Với hơn 1.600 hòn đảo đá vôi nhấp nhô trên mặt nước xanh biếc, Vịnh Hạ Long tạo nên một khung cảnh hùng vĩ và thơ mộng. Du khách có thể tham gia tour du thuyền qua đêm, khám phá các hang động kỳ bí như hang Sung Sót, hang Đầu Gỗ, hoặc thử sức với các hoạt động thể thao nước như chèo kayak.

Sapa, thị trấn miền núi nằm ở độ cao 1.500m so với mặt nước biển, là thiên đường của những ai yêu thích khí hậu mát mẻ và cảnh quan núi non hùng vĩ. Ruộng bậc thang Sapa được UNESCO công nhận là di sản văn hóa thế giới, tạo nên những bức tranh thiên nhiên tuyệt đẹp thay đổi theo mùa. Mùa nước đổ (tháng 5-6), ruộng bậc thang như những tấm gương khổng lồ phản chiếu bầu trời. Mùa lúa chín (tháng 9-10), cả thung lũng chuyển sang màu vàng óng của lúa chín.

Ninh Bình được mệnh danh là "Vịnh Hạ Long trên cạn" với quần thể danh thắng Tràng An. Nơi đây có hệ thống hang động, sông ngầm chạy xuyên qua những dãy núi đá vôi tạo nên cảnh quan kỳ thú. Du khách có thể đi thuyền khám phá các hang động như hang Sáng, hang Tối, hang Nấu Rượu, mỗi hang đều có những nét đẹp riêng biệt.

Miền Trung Việt Nam - Cầu nối văn hóa và lịch sử

Huế, cố đô của triều Nguyễn, là nơi lưu giữ nhiều di tích lịch sử văn hóa quý báu. Đại Nội Huế với Hoàng thành, Tử cấm thành và các lăng tẩm của các vua triều Nguyễn là minh chứng cho sự huy hoàng của văn hóa Việt Nam thời phong kiến. Sông Hương thơ mộng với những chuyến du ngoạn bằng thuyền rồng, thưởng thức ca Huế và ngắm cảnh chùa Thiên Mụ cổ kính.

Hội An, phố cổ được UNESCO công nhận là di sản văn hóa thế giới, là điểm đến lý tưởng cho những ai muốn tìm hiểu về kiến trúc cổ Việt Nam. Phố cổ Hội An với những ngôi nhà cổ có kiến trúc độc đáo, pha trộn giữa văn hóa Việt, Trung, Nhật tạo nên một không gian văn hóa đa dạng và phong phú. Chùa Cầu Nhật Bản, nhà cổ Tấn Ký, hội quán Phúc Kiến là những điểm tham quan không thể bỏ qua.

Mỹ Sơn, thánh địa của vương quốc Chăm Pa cổ, là quần thể các tháp Chăm được xây dựng từ thế kỷ 4 đến thế kỷ 14. Nơi đây lưu giữ những giá trị văn hóa, tôn giáo độc đáo của dân tộc Chăm, với kiến trúc tháp Chăm tinh xảo và những bức điêu khắc nghệ thuật tuyệt đẹp.

Đà Nẵng, thành phố đáng sống bậc nhất Việt Nam, sở hữu những bãi biển đẹp nhất thế giới như bãi biển Mỹ Khê. Bán đảo Sơn Trà với ngôi chùa Linh Ứng và tượng Phật Quan Âm cao 67m là điểm đến tâm linh hấp dẫn. Bà Nà Hills với cây cầu Vàng nổi tiếng thế giới đã trở thành biểu tượng du lịch mới của Việt Nam.

Phong Nha - Kẻ Bàng, công viên quốc gia được UNESCO công nhận là di sản thiên nhiên thế giới, sở hữu hệ thống hang động khổng lồ và đa dạng nhất thế giới. Hang Sơn Trà, hang Phong Nha, hang Thiên Đường với những khối thạch nhũ kỳ vĩ tạo nên cung điện thiên nhiên tuyệt đẹp.

Miền Nam Việt Nam - Vùng đất năng động và phồn thịnh

Thành phố Hồ Chí Minh, trung tâm kinh tế lớn nhất Việt Nam, là nơi giao thoa giữa truyền thống và hiện đại. Quận 1 với những tòa nhà cao tầng hiện đại đan xen cùng các công trình kiến trúc Pháp cổ kính như Nhà hát Thành phố, Bưu điện Trung tâm, Nhà thờ Đức Bà tạo nên một đô thị đa sắc màu.

Chợ Bến Thành, biểu tượng của Sài Gòn, là nơi du khách có thể mua sắm các sản phẩm đặc trưng của Việt Nam từ áo dài, tranh sơn mài, đến các loại gia vị, cà phê Việt Nam. Khu phố Tây Bùi Viện với cuộc sống về đêm náo nhiệt, các quán bar, nhà hàng đa quốc gia thu hút đông đảo du khách quốc tế.

Đồng bằng sông Cửu Long, vùng đất màu mỡ với hệ thống kênh rạch chằng chịt, là nơi trải nghiệm cuộc sống miền Tây Nam Bộ đậm chất sông nước. Chợ nổi Cái Răng, chợ nổi Phong Điền là những điểm đến độc đáo cho phép du khách khám phá văn hóa sông nước đặc trưng.

Cần Thơ, thành phố trung tâm của vùng đồng bằng sông Cửu Long, nổi tiếng với chợ nổi Cái Răng sầm uất. Du khách có thể thưởng thức các đặc sản miền Tây như cơm dẻo, bánh xèo, lẩu mắm, trái cây nhiệt đới tươi ngon.

Đảo Phú Quốc, hòn ngọc của vịnh Thái Lan, là điểm đến lý tưởng cho những ai muốn nghỉ dưỡng bên bãi biển tuyệt đẹp. Bãi biển Sao với cát trắng mịn như bột, nước biển trong xanh, bãi biển Ông Lang yên tĩnh với những resort cao cấp là nơi thư giãn hoàn hảo.

Côn Đảo, quần đảo với 16 hòn đảo lớn nhỏ, không chỉ là nơi có ý nghĩa lịch sử với nhà tù Côn Đảo mà còn là thiên đường du lịch sinh thái với rạn san hô đa dạng, bãi biển hoang sơ và làn nước biển trong xanh như pha lê.

Vũng Tàu, thành phố biển gần Sài Gòn, là điểm đến cuối tuần lý tưởng với bãi biển Thùy Vân, núi Tao Phùng và tượng Chúa Kitô vua cao 32m nhìn ra biển cả bao la.

Ẩm thực Việt Nam - Tinh hoa văn hóa ẩm thực

Ẩm thực Việt Nam được UNESCO công nhận là di sản văn hóa phi vật thể của nhân loại với sự đa dạng về hương vị từ Bắc vào Nam. Phở Hà Nội với nước dùng thanh đạm, thơm mùi thảo quả và hành tây, khác biệt hoàn toàn với phở Sài Gòn có nước dùng đậm đà, ăn kèm với nhiều rau sống.

Bún bò Huế với nước lèo cay nồng đặc trưng, bánh khoái, bánh bèo, bánh ít là những món ăn mang đậm dấu ấn cố đô. Cao lầu Hội An, bánh mì Hội An với sự kết hợp độc đáo giữa các nguyên liệu tạo nên hương vị không thể nhầm lẫn.

Cơm tấm Sài Gòn, bánh xèo miền Tây, lẩu mắm, hủ tiếu Nam Vang là những món ăn đặc trưng của miền Nam với hương vị đậm đà, cay nồng. Bánh mì Việt Nam, được CNN bình chọn là một trong những món ăn đường phố ngon nhất thế giới, với vỏ bánh giòn rụm, nhân đa dạng từ pate, chả cá, thịt nướng đến chả cá.

Cà phê Việt Nam với phong cách pha chế độc đáo bằng phin nhỏ giọt, tạo nên hương vị đậm đà, thơm lừng. Cà phê sữa đá, cà phê đen, bạc xỉu là những thức uống không thể thiếu trong văn hóa cà phê Việt Nam.

Lễ hội và văn hóa truyền thống

Tết Nguyên Đán, lễ hội lớn nhất trong năm của người Việt Nam, là dịp để gia đình sum họp, thờ cúng tổ tiên và cầu chúc một năm mới an khang, thịnh vượng. Không khí Tết với những cành đào, cành mai nở rộ, bánh chưng, bánh tét truyền thống tạo nên không gian văn hóa đặc sắc.

Lễ hội Đền Hùng, tưởng nhớ các vua Hùng - những người có công dựng nước, được tổ chức hằng năm vào ngày 10 tháng 3 âm lịch tại Phú Thọ. Lễ hội chùa Hương, lễ hội Gióng, lễ hội Đăng Đèn tại Hội An là những sự kiện văn hóa truyền thống thu hút hàng triệu lượt khách tham quan.

Áo dài Việt Nam, trang phục truyền thống với những đường cong uyển chuyển, thanh lịch, là biểu tượng của người phụ nữ Việt Nam. Nón lá, chiếc nón truyền thống được làm từ lá cọ, không chỉ là vật dụng che nắng mưa mà còn là tác phẩm nghệ thuật thủ công tinh xảo.

Làng nghề truyền thống như làng gốm Bát Tràng, làng lụa Vạn Phúc, làng tranh Đông Hồ vẫn duy trì và phát triển các nghề thủ công mỹ nghệ truyền thống của dân tộc.

Thiên nhiên và khí hậu

Việt Nam có khí hậu nhiệt đới gió mùa với hai mùa rõ rệt: mùa khô và mùa mưa. Mỗi vùng miền có đặc điểm khí hậu riêng biệt, tạo nên sự đa dạng về cảnh quan thiên nhiên.

Miền Bắc có bốn mùa rõ rệt: xuân ấm áp, hạ nóng ẩm, thu mát mẻ, đông lạnh. Mùa thu Hà Nội với những hàng phượng vĩ vàng rụng, mùa đông Sapa với băng giá phủ trắng đỉnh Fansipan là những trải nghiệm thú vị.

Miền Trung có khí hậu chuyển tiếp với mùa mưa bão từ tháng 9 đến tháng 12, nhưng cũng có những tháng nắng đẹp lý tưởng cho du lịch biển. Miền Nam có khí hậu nhiệt đới với hai mùa mưa khô rõ rệt, thích hợp cho du lịch quanh năm.

Việt Nam sở hữu hệ sinh thái đa dạng từ rừng nhiệt đới, rừng mưa đến các vùng ngập mặn, san hô biển. Vườn quốc gia Phong Nha - Kẻ Bàng, vườn quốc gia Cát Tiên, vườn quốc gia Ba Vì là những khu bảo tồn thiên nhiên quan trọng."""


qdrant_service.update(docs)