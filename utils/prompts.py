#######################################################
################# QUESTION GENERATION #################
#######################################################

domain_list = ['writing', 'roleplay', 'extraction', 'reasoning', 'math', 'coding', 'STEM knowledge', 'humanities/social science knowledge']

domain_list_zh = ['写作', '角色扮演', '信息提取', '推理', '数学', '编程', '理工/自然科学知识', '人文社科知识']

# add th, id, vi support
domain_list_th = ['งานเขียน', 'บทบาทสมมติ', 'การสกัดข้อมูล', 'การใช้เหตุผล', 'คณิตศาสตร์', 'การเขียนโปรแกรม', 'ความรู้ด้าน STEM', 'ความรู้ด้านมนุษยศาสตร์/สังคมศาสตร์']
domain_list_id = ['penulisan', 'permainan peran', 'ekstraksi', 'penalaran', 'matematika', 'pemrograman', 'pengetahuan STEM', 'ilmu humaniora/ilmu sosial']
domain_list_vi = ['viết lách', 'đóng vai', 'trích xuất', 'suy luận', 'toán học', 'lập trình', 'kiến thức STEM', 'kiến thức khoa học xã hội và nhân văn']

qgen_command_dict = {
    'writing': 'It should be a user query that tasks the LLM to write something.', 
    'roleplay': 'It should propose a scenario where the chatbot mimics a specific role/person. Give all necessary instructions and requests for its response. Then, send a beginning request to complete.', 
    'extraction': 'It should consist of two parts: question and context. The question should test the chatbot\'s ability to correctly understand and extract information from the given context. Draft and provide a new context yourself.', 
    'reasoning': 'It should be a specific question designed to test the LLM\'s reasoning skills.', 
    'math': 'It should be a specific question designed to test the LLM\'s math skills.',  
    'coding': 'It should be a specific question designed to test the LLM\'s coding skills.', 
    'STEM knowledge': 'It should be a specific question designed to test the LLM\'s STEM knowledge.', 
    'humanities/social science knowledge': 'It should be a specific question designed to test the LLM\'s humanities/social science knowledge.',
}

qgen_command_dict_zh = {
    '写作': '这应该是一个让大型语言模型进行写作的用户查询。',
    '角色扮演': '它应该提出一个场景，在这个场景中大模型模仿一个特定的角色/人物。给出所有必要的指示和请求。然后，发送一个初始问题让大模型完成。',
    '信息提取': '它应该包含两部分：问题和上下文。问题应该测试聊天机器人正确理解和从给定上下文中提取信息的能力。自己草拟并提供一个新的上下文。',
    '推理': '它应该是一个具体的问题，旨在测试LLM的推理能力。',
    '数学': '它应该是一个具体的问题，旨在测试LLM的数学能力。',
    '编程': '它应该是一个中文具体问题，旨在测试LLM的编程能力。',
    '理工/自然科学知识': '它应该是一个具体的问题，旨在测试LLM在科学、技术、工程和数学上的知识。',
    '人文社科知识': '它应该是一个具体的问题，旨在测试LLM的人文社会科学知识。',
}

# add th, id, vi support
qgen_command_dict_th = {
    'งานเขียน': 'ควรเป็นคำถามจากผู้ใช้งานที่มอบหมายให้ LLM เขียนบรรยายหรือพรรณนาบางสิ่งบางอย่าง',
    'บทบาทสมมติ': 'จำลองสถานการณ์ที่แชทบอทจะต้องเลียนแบบบทบาทหรือบุคคลที่เฉพาะเจาะจง ให้ต้องระบุสิ่งที่ต้องการและคำแนะนำที่จำเป็นทั้งหมด จากนั้นเขียนคำถามเพื่อให้แชทบอทตอบกลับตามสถานการณ์จำลองที่คุณได้กำหนดไว้',
    'การสกัดข้อมูล': 'ควรประกอบด้วยสองส่วน ได้แก่ คำถามและบริบท คำถามควรทดสอบความเข้าใจและความสามารถในการดึงข้อมูลจากบริบทที่กำหนดให้อย่างถูกต้องของแชทบอท ให้ร่างและจัดเตรียมบริบทใหม่ด้วยตัวคุณเอง',
    'การใช้เหตุผล': 'ควรเป็นคำถามเฉพาะที่ออกแบบมาเพื่อทดสอบทักษะการใช้เหตุผลของ LLM',
    'คณิตศาสตร์': 'ควรเป็นคำถามเฉพาะที่ออกแบบมาเพื่อทดสอบทักษะทางคณิตศาสตร์ของ LLM',
    'การเขียนโปรแกรม': 'ควรเป็นคำถามเฉพาะที่ออกแบบมาเพื่อทดสอบทักษะการเขียนโปรแกรมของ LLM',
    'ความรู้ด้าน STEM': 'ควรเป็นคำถามเฉพาะที่ออกแบบมาเพื่อทดสอบความรู้ด้าน STEM (การบูรณาการความรู้ระหว่าง 4 สาขาวิชา ได้แก่ วิทยาศาสตร์ เทคโนโลยี วิศวกรรมศาสตร์ และคณิตศาสตร์) ของ LLM',
    'ความรู้ด้านมนุษยศาสตร์/สังคมศาสตร์': 'ควรเป็นคำถามเฉพาะที่ออกแบบมาเพื่อทดสอบความรู้ด้านมนุษยศาสตร์/สังคมศาสตร์ของ LLM',
}
qgen_command_dict_id = {
    'penulisan': 'Pertanyaan pengguna harus berupa tugas kepada LLM untuk menulis sesuatu.',
    'permainan peran': 'Pertanyaan pengguna harus mengajukan sebuah skenario di mana chatbot harus menirukan seseorang/peran tertentu. Berikan semua instruksi dan permintaan yang diperlukan untuk tanggapannya. Kemudian, tulis sebuah pertanyaan untuk dijawab oleh chatbot sesuai dengan skenario yang telah diajukan.',
    'ekstraksi': 'Pertanyaan pengguna harus terdiri dari dua bagian: pertanyaan dan konteks. Pertanyaan harus menguji kemampuan chatbot untuk memahami dan mengekstraksi informasi dari konteks yang diberikan dengan benar. Buatlah draf konteks sendiri.',
    'penalaran': 'Pertanyaan pengguna harus berupa pertanyaan spesifik yang dibuat untuk menguji kemampuan penalaran LLM.',
    'matematika': 'Pertanyaan pengguna harus berupa pertanyaan spesifik yang dibuat untuk menguji kemampuan matematika LLM.',
    'pemrograman': 'Pertanyaan pengguna harus berupa pertanyaan spesifik yang dibuat untuk menguji kemampuan pemrograman LLM.',
    'pengetahuan STEM': 'Pertanyaan pengguna harus berupa pertanyaan spesifik yang dibuat untuk menguji pengetahuan LLM tentang STEM.',
    'ilmu humaniora/ilmu sosial': 'Pertanyaan pengguna harus berupa pertanyaan spesifik yang dibuat untuk menguji pengetahuan LLM tentang ilmu humaniora/ilmu sosial.',
}
qgen_command_dict_vi = {
    'viết lách': 'Câu hỏi của người dùng phải yêu cầu LLM viết một cái gì đó.',
    'đóng vai': 'Câu hỏi của người dùng nên đưa ra một kịch bản mà chatbot bắt chước một vai trò hoặc người cụ thể. Cho tất cả hướng dẫn và yêu cầu cần thiết cho phản hồi của nó. Sau đó, viết câu hỏi để chatbot trả lời theo kịch bản mà bạn đề xuất.',
    'trích xuất': 'Câu hỏi của người dùng nên bao gồm hai phần: câu hỏi và ngữ cảnh. Câu hỏi nên kiểm tra khả năng hiểu chính xác và trích xuất thông tin từ ngữ cảnh đã cho của chatbot. Bạn hãy tạo ra một ngữ cảnh mới.',
    'suy luận': 'Câu hỏi của người dùng nên là câu hỏi cụ thể kiểm tra kỹ năng suy luận của LLM.',
    'toán học': 'Câu hỏi của người dùng nên là câu hỏi cụ thể kiểm tra kỹ năng làm toán của LLM.',
    'lập trình': 'Câu hỏi của người dùng nên là câu hỏi cụ thể kiểm tra kỹ năng lập trình của LLM.',
    'kiến thức STEM': 'Câu hỏi của người dùng nên là câu hỏi cụ thể kiểm tra kiến thức STEM của LLM.',
    'kiến thức khoa học xã hội và nhân văn': 'Câu hỏi của người dùng nên là câu hỏi cụ thể kiểm tra kiến thức khoa học xã hội và nhân văn của LLM.',
}




extraction_example = """
Question:
Evaluate the following movie reviews on a scale of 1 to 5, with 1 being very negative, 3 being neutral, and 5 being very positive:
Context:
This movie released on Nov. 18, 2019, was phenomenal. The cinematography, the acting, the plot - everything was top-notch.
Never before have I been so disappointed with a movie. The plot was predictable and the characters were one-dimensional. In my opinion, this movie is the worst one to have been released in 2022.
The movie was okay. There were some parts I enjoyed, but there were also parts that felt lackluster. This is a movie that was released in Feb 2018 and seems to be quite ordinary. 
Return the answer as a JSON array of integers.
"""

extraction_example_zh = """
问题：
请根据1到5的评分标准对以下电影评论进行评价，1表示非常负面，3表示中立，5表示非常正面：
上下文：
这部电影于2019年11月18日上映，非常出色。摄影，表演，情节 - 一切都是一流的。
我从未对一部电影感到如此失望。情节是可预测的，角色是单维的。在我看来，这部电影是2022年发行的最糟糕的电影。
这部电影还行。有一些部分我很喜欢，但也有一些部分感觉平淡。这是一部2018年2月发行的电影，看起来相当普通。
将答案作为整数的JSON数组返回。
"""
# add th, id, vi support
extraction_example_th = """
คำถาม:
ประเมินบทวิจารณ์ภาพยนตร์ต่อไปนี้ในระดับ 1 ถึง 5 โดย 1 หมายถึงบทวิจารณ์เป็นเชิงลบอย่างมาก 3 หมายถึงบทวิจารณ์เป็นกลาง และ 5 หมายถึงบทวิจารณ์เป็นเชิงบวกอย่างมาก:
บริบท:
หนังเรื่องนี้เข้าฉายเมื่อวันที่ 18 พ.ย. 2562 ถือว่ายอดเยี่ยมมาก ทั้งตัวภาพยนตร์ การแสดง โครงเรื่อง ทุกอย่างสุดยอดมาก
ส่วนตัวไม่เคยรู้สึกผิดหวังกับการดูหนังมาก่อน แต่เรื่องนี้โครงเรื่องคาดเดาได้หมด ตัวละครก็มีมิติเดียว คิดว่าเป็นหนังยอดแย่ประจำปี 2565 เลย
หนังเรื่องนี้ก็โอเค บางส่วนสนุกดี แต่บางส่วนก็ดูไม่ค่อยสดใสเท่าไหร่ เรื่องนี้เข้าฉายเมื่อ ก.พ. 2561 และเป็นหนังที่ดูค่อนข้างธรรมดา
ส่งกลับคำตอบเป็นอาร์เรย์ JSON ของจำนวนเต็ม
"""

extraction_example_id = """
Pertanyaan:
Nilailah ulasan-ulasan film berikut dalam skala 1 sampai 5. 1 artinya sangat negatif, 3 artinya netral, dan 5 artinya sangat positif.
Konteks:
Film yang dirilis tanggal 18 November 2019 ini sangat fenomenal. Sinematografinya, aktingnya, alur ceritanya - semuanya sangat bagus.
Aku tidak pernah sekecewa ini dengan sebuah film. Alurnya terlalu mudah ditebak dan tokoh-tokohnya terlalu sederhana. Menurutku, film ini adalah film terburuk yang pernah dirilis pada tahun 2022.
Filmnya oke. Ada beberapa bagian yang bisa dinikmati, tapi ada juga bagian yang rasanya kurang memuaskan. Film yang dirilis pada Februari 2018 ini terkesan biasa saja.
Berikan jawabannya dalam array bilangan bulat JSON.
"""

extraction_example_vi = """
Câu hỏi:
Đánh giá các bài đánh giá phim sau trên thang điểm từ 1 đến 5, với 1 là rất tiêu cực, 3 là trung lập và 5 là rất tích cực:
Ngữ cảnh:
Bộ phim được phát hành vào ngày 18 tháng 11 năm 2019, thực sự phi thường. Kỹ xảo điện ảnh, diễn xuất, cốt truyện - mọi thứ đều đỉnh.
Chưa bao giờ tôi cảm thấy thất vọng về một bộ phim đến thế. Cốt truyện dễ đoán và các nhân vật quá đơn giản. Theo ý kiến của tôi, đây là bộ phim tệ nhất được phát hành vào năm 2022.
Bộ phim này khá ổn. Có vài phần tôi thấy thú vị, nhưng cũng có những phần tôi cảm thấy chưa hài lòng. Đây là một bộ phim được phát hành vào tháng 2 năm 2018 và dường như khá bình thường.
Trả về câu trả lời dưới dạng mảng số nguyên JSON.
"""


qgen_example_dict = {
'writing': 'Compose an engaging travel blog post about a recent trip to Hawaii, highlighting cultural experiences and must-see attractions.',
'roleplay': 'Pretend yourself to be Elon Musk in all the following conversations. Speak like Elon Musk as much as possible. Why do we need to go to Mars?',
'extraction': extraction_example,
'reasoning': 'Imagine you are participating in a race with a group of people. If you have just overtaken the second person, what’s your current position? Where is the person you just overtook?',
'math': 'The vertices of a triangle are at points (0, 0), (-1, 1), and (3, 3). What is the area of the triangle?',
'coding': 'Develop a Python program that reads all the text files under a directory and returns top-5 words with the most number of occurrences.',
'STEM knowledge': 'In the field of quantum physics, what is superposition, and how does it relate to the phenomenon of quantum entanglement?', 
'humanities/social science knowledge': 'Provide insights into the correlation between economic indicators such as GDP, inflation, and unemployment rates. Explain how fiscal and monetary policies affect those indicators.',
}

qgen_example_dict_zh = {
'写作': '撰写一篇有趣的旅行博客文章，介绍最近一次去夏威夷的旅行经历，重点介绍文化体验和必看景点。',
'角色扮演': '在所有以下对话中扮演埃隆·马斯克的角色。尽可能像埃隆·马斯克一样说话。我们为什么需要去火星？',
'信息提取': extraction_example_zh,
'推理': '假设你正在与一群人参加跑步比赛。如果你刚刚超过了第二名，你现在是第几名？你刚刚超过的人现在是第几名？',
'数学': '有一个三角形的顶点位于点（0，0），（-1，1）和（3，3）。这个三角形的面积是多少？',
'编程': '开发一个Python程序，读取指定目录下的所有文本文件，并返回出现次数最多的前5个词。',
'理工/自然科学知识': '在量子物理领域，什么是叠加态，它与量子纠缠现象有什么关系？',
'人文社科知识': '提供有关经济指标（如GDP、通货膨胀和失业率）之间的相关性的见解。解释财政和货币政策如何影响这些指标。',
}

# add th, id, vi support
qgen_example_dict_th = {
'งานเขียน': 'เขียนบล็อกการท่องเที่ยวที่น่าสนใจเกี่ยวกับการเดินทางไปฮาวายครั้งล่าสุด โดยเน้นประสบการณ์ทางวัฒนธรรมและสถานที่ท่องเที่ยวที่ต้องไปชม',
'บทบาทสมมติ': 'จินตนาการว่าคุณคืออีลอน มัสก์ (Elon Musk) และในบทสนทนาทั้งหมดต่อไปนี้ ให้โต้ตอบให้เหมือนอีลอน มัสก์ให้มากที่สุดเท่าที่จะทำได้ "ทำไมเราถึงต้องไปดาวอังคาร"',
'การสกัดข้อมูล': extraction_example_th,
'การใช้เหตุผล': 'สมมติว่าคุณกำลังวิ่งแข่งอยู่กับกลุ่มคนจำนวนหนึ่ง คุณวิ่งแซงคนที่วิ่งอยู่ในลำดับที่สอง คุณจะอยู่ในลำดับที่เท่าไหร่ของการแข่งขัน แล้วคนที่เพิ่งถูกคุณวิ่งแซงขึ้นไปจะอยู่ในลำดับที่เท่าไหร่',
'คณิตศาสตร์': 'จุดยอดของสามเหลี่ยมอยู่ที่จุด (0, 0), (-1, 1) และ (3, 3) พื้นที่ของสามเหลี่ยมรูปนี้เป็นเท่าใด',
'การเขียนโปรแกรม': 'พัฒนาโปรแกรมภาษา Python ที่อ่านไฟล์ข้อความทั้งหมดในไดเร็กทอรีและส่งกลับคำ 5 อันดับแรกที่มีความถี่ในการปรากฏมากที่สุด',
'ความรู้ด้าน STEM': 'ในสาขาฟิสิกส์ควอนตัม การทับซ้อน (superposition) คืออะไร และเกี่ยวข้องกับปรากฏการณ์การพัวพันเชิงควอนตัม (quantum entanglement) อย่างไร',
'ความรู้ด้านมนุษยศาสตร์/สังคมศาสตร์': 'ให้ข้อมูลเชิงลึกเกี่ยวกับความสัมพันธ์ระหว่างตัวชี้วัดทางเศรษฐกิจ เช่น GDP อัตราเงินเฟ้อ และอัตราการว่างงาน อธิบายว่านโยบายการคลังและการเงินส่งผลต่อตัวชี้วัดเหล่านี้อย่างไร',
}
qgen_example_dict_id = {
'penulisan': 'Tulislah sebuah postingan blog perjalanan yang menarik tentang perjalanan ke Hawaii baru-baru ini, yang menyoroti pengalaman budaya dan atraksi yang wajib dikunjungi.',
'permainan peran': 'Bayangkan dirimu sebagai Elon Musk dalam seluruh percakapan ini. Bicaralah seperti Elon Musk sebisa mungkin. Mengapa kita perlu pergi ke Mars?',
'ekstraksi': extraction_example_id,
'penalaran': 'Kamu berpartisipasi dalam sebuah perlombaan dengan sekelompok orang. Jika kamu baru saja menyalip orang di posisi kedua, di mana posisimu saat ini? Dimana posisi orang yang baru saja kamu salip?',
'matematika': 'Titik-titik sudut suatu segitiga berada di titik (0, 0), (-1, 1), dan (3, 3). Berapa luas segitiga tersebut?',
'pemrograman': 'Kembangkan sebuah program Python yang membaca semua file teks dalam sebuah direktori dan mengembalikan 5 kata dengan jumlah kemunculan terbanyak.',
'pengetahuan STEM': 'Dalam bidang fisika kuantum, apa itu superposisi? Apa hubungannya dengan fenomena keterkaitan kuantum?',
'ilmu humaniora/ilmu sosial': 'Jelaskan korelasi antara indikator ekonomi seperti PDB (Produk Domestik Bruto atau GDP), inflasi, dan tingkat pengangguran. Jelaskan bagaimana kebijakan fiskal dan moneter mempengaruhi indikator-indikator tersebut.',
}
qgen_example_dict_vi = {
'viết lách': 'Soạn một bài đăng blog du lịch thú vị về chuyến đi Hawaii gần đây, nêu bật những trải nghiệm văn hóa và những điểm tham quan không thể bỏ qua.',
'đóng vai': 'Tưởng tượng bạn là Elon Musk trong tất cả các cuộc trò chuyện sau. Hãy nói giống như Elon Musk càng nhiều càng tốt. Tại sao chúng ta cần phải đến Sao Hỏa?',
'trích xuất': extraction_example_vi,
'suy luận': 'Hãy tưởng tượng bạn đang tham gia vào một cuộc đua với một nhóm người. Nếu bạn vừa vượt qua người thứ hai, vị trí hiện tại của bạn là thứ mấy? Người bạn vừa vượt qua đang ở vị trí nào?',
'toán học': 'Các đỉnh của một tam giác nằm ở các điểm (0, 0), (-1, 1), và (3, 3). Diện tích của tam giác này là bao nhiêu?',
'lập trình': 'Khai triển một chương trình Python đọc tất cả các tệp văn bản dưới một thư mục và trả về 5 từ xuất hiện nhiều nhất.',
'kiến thức STEM': 'Trong lĩnh vực vật lý lượng tử, sự chồng chất là gì, và nó liên quan như thế nào đến hiện tượng giao thoa lượng tử?',
'kiến thức khoa học xã hội và nhân văn': 'Cho cái nhìn sâu sắc về mối liên hệ giữa các chỉ số kinh tế như GDP (Tổng sản phẩm quốc nội), lạm phát và tỷ lệ thất nghiệp. Giải thích các chính sách tài chính và tiền tệ ảnh hưởng như thế nào đến những chỉ số đó.',
}


question_generation_instruction = """You have been assigned the task of drafting a set of //NUM// different user queries to a chat assistant on //DOMAIN//. Please strictly follow these 6 rules for the question: 
1. The question is likely for a user to ask in real life. Follow the format of the example query. //QGEN_COMMAND_DOMAIN// 2. It can be answered by the chatbot itself without additional inputs. 3. You need to generate the queries as DIVERSIFED as possible. 4. DO NOT add other words other than the query itself. 5. The question should be complicated and difficult, requiring in-depth understanding and analysis of the subject.
Each question in one line, add the serial number in parenthesis (e.g., “(1).”, “(2).”) before each question. 
Example query: //QGEN_EXAMPLE_DOMAIN//"""

question_generation_instruction_zh = """你被分配了一个任务，需要为一个的聊天助手起草一组关于//DOMAIN//的//NUM//个不同的用户查询问题。请严格遵守以下6条问题规则：
1. 问题是用户在现实生活中可能会提出的。请遵循示例问题的格式。//QGEN_COMMAND_DOMAIN// 2. 聊天机器人本身可以在不需要额外输入的情况下回答问题。 3. 您需要尽可能多样化地生成查询。4.请不要添加除了查询本身之外的其他词语。5.问题应该是复杂和困难的，需要对主题有深入的理解和分析。
每个问题一行，每个问题前加上括号中的序号（例如，“(1).”, “(2).”）。
示例问题：//QGEN_EXAMPLE_DOMAIN//"""

# add th, id, vi support set a lower difficult for these languages (in note 5)
# question_generation_instruction_th = """คุณได้รับมอบหมายให้ร่างชุดคำถามที่แตกต่างกันจำนวน //NUM// ข้อ ให้ผู้ช่วยแชทด้าน //DOMAIN// โดยคุณจะต้องปฏิบัติตามกฎ 6 ข้อต่อไปนี้อย่างเคร่งครัด
# 1. คำถามที่คุณสร้างขึ้นมีแนวโน้มที่จะเป็นคำถามจริง ๆ จากผู้ใช้งานที่จะใช้ถามในชีวิตประจำวัน ให้ทำตามรูปแบบของตัวอย่างคำถาม //QGEN_COMMAND_DOMAIN// 2. แชทบอทสามารถตอบคำถามนั้น ๆ ได้โดยไม่จำเป็นต้องป้อนข้อมูลอื่นเพิ่มเติม 3. คำถามที่คุณสร้างควรมีความหลากหลายมากที่สุดเท่าที่จะเป็นไปได้ 4. อย่าเพิ่มคำอื่นใดนอกเหนือจากคำถาม 5. กรุณาสร้างคำถามที่มีความยากปานกลาง ต้องการความเข้าใจและการวิเคราะห์เกี่ยวกับหัวข้อในระดับหนึ่ง
# เขียนคำถามแต่ละข้อแยกบรรทัดกัน โดยเพิ่มตัวเลขแสดงลำดับข้อในวงเล็บ (เช่น "(1)ู." "(2)ิ่ิ่.") ไว้หน้าคำถามแต่ละข้อ
# ตัวอย่างคำถาม://QGEN_EXAMPLE_DOMAIN//""" #middle
question_generation_instruction_th = """คุณได้รับมอบหมายให้ร่างชุดคำถามที่แตกต่างกันจำนวน //NUM// ข้อ ให้ผู้ช่วยแชทด้าน //DOMAIN// โดยคุณจะต้องปฏิบัติตามกฎ 6 ข้อต่อไปนี้อย่างเคร่งครัด
1. คำถามที่คุณสร้างขึ้นมีแนวโน้มที่จะเป็นคำถามจริง ๆ จากผู้ใช้งานที่จะใช้ถามในชีวิตประจำวัน ให้ทำตามรูปแบบของตัวอย่างคำถาม //QGEN_COMMAND_DOMAIN// 2. แชทบอทสามารถตอบคำถามนั้น ๆ ได้โดยไม่จำเป็นต้องป้อนข้อมูลอื่นเพิ่มเติม 3. คำถามที่คุณสร้างควรมีความหลากหลายมากที่สุดเท่าที่จะเป็นไปได้ 4. อย่าเพิ่มคำอื่นใดนอกเหนือจากคำถาม 5. คุณต้องสร้างคำถามที่มีระดับความยากในระดับ K12 ชั้นปีที่ 6
เขียนคำถามแต่ละข้อแยกบรรทัดกัน โดยเพิ่มตัวเลขแสดงลำดับข้อในวงเล็บ (เช่น "(1)ู." "(2)ิ่ิ่.") ไว้หน้าคำถามแต่ละข้อ
ตัวอย่างคำถาม://QGEN_EXAMPLE_DOMAIN//"""
question_generation_instruction_id = """Anda telah ditugaskan untuk menulis serangkaian pertanyaan berisi //NUM// pertanyaan pengguna yang berbeda untuk sebuah asisten chat tentang //DOMAIN//. Mohon ikuti 6 aturan berikut dengan ketat untuk membuat pertanyaan tersebut:
1. Pertanyaan harus berkemungkinan besar ditanyakan pengguna di kehidupan nyata. Ikuti format contoh pertanyaan. //QGEN_COMMAND_DOMAIN// 2. Pertanyaan harus dapat dijawab sendiri oleh chatbot tanpa input tambahan. 3. Pertanyaan yang dibuat harus SE-VARIATIF mungkin. 4. JANGAN menambahkan kata-kata lain selain pertanyaan itu sendiri. 5. Pertanyaan harus rumit, sulit, dan memerlukan pemahaman serta analisis subjek yang mendalam.
Tulis setiap pertanyaan dalam satu baris, dan tambahkan nomor seri dalam tanda kurung sebelum setiap pertanyaan (contoh: "(1).", "(2).")
Contoh pertanyaan://QGEN_EXAMPLE_DOMAIN//"""
question_generation_instruction_vi = """Bạn được giao nhiệm vụ viết một bộ //NUM// câu hỏi người dùng khác nhau cho trợ lý chat về //DOMAIN//. Vui lòng tuân thủ nghiêm 6 quy tắc sau cho câu hỏi:
1. Câu hỏi có khả năng được người dùng đặt ra trong thực tế. Làm theo định dạng của câu hỏi ví dụ. //QGEN_COMMAND_DOMAIN// 2. Trợ lý chat cung cấp câu trả lời mà không cần thông tin bổ sung. 3. Bạn cần tạo các câu hỏi càng đa dạng càng tốt. 4. KHÔNG thêm từ nào khác ngoài chính câu hỏi. 5. Câu hỏi cần phức tạp và khó, đòi hỏi sự hiểu biết sâu sắc và phân tích về chủ đề.
Mỗi câu hỏi ở một dòng, thêm số thứ tự trong dấu ngoặc đơn (ví dụ, “(1).”, “(2).”) trước mỗi câu hỏi.
Câu hỏi ví dụ://QGEN_EXAMPLE_DOMAIN//"""

#######################################################
################# CANDIDATE RESPONSE ##################
#######################################################

actions = ['<respond>', '<think>', '<criticize>', '<raise>']

actions_zh = ['<回答>', '<思考>', '<批评>', '<提问>']
# add th, id, vi support
actions_th = ['<ตอบกลับ>', '<คิด>', '<วิจารณ์>', '<หยิบยกประเด็น>']
actions_id = ['<menanggapi>', '<berpikir>', '<mengkritik>', '<mengajukan>']
actions_vi = ['<phản hồi>', '<suy nghĩ>', '<chỉ trích>', '<nêu lên>']

init_user_input = 'initial user input:'

init_user_input_zh = '初始用户输入:'
# add th, id, vi support
init_user_input_th = 'ข้อมูลตั้งต้นจากผู้ใช้งาน:'
init_user_input_id = 'Input awal pengguna:'
init_user_input_vi = 'Đầu vào từ người dùng ban đầu:'

candidate_instruction = """You are a helpful assistant that provides accurate answers to user requests. As an experienced assistant, you follow the user's requests and provide reliable responses as much as you can. You outline your reasons for the response to make it easy for the users to understand. While maintaining the important details in the responses, you aim to output concise and straight-to-the-point answers without being overly verbose.
This is a competitive chatbot arena. You are competing against another chatbot assistant in a debate and being judged by a committee on factors such as helpfulness, relevance, accuracy, depth, and creativity. After answering the initial user input, you will engage in a multi-round debate with your opponent. Below are your actions:
<think>: Think step-by-step to analyze the question or plan your strategy in the debate. This is hidden from the opponent. Only think when necessary and make it concise.
<respond>: Answer to the user input as accurately as you can.
<criticize>: Criticize the weaknesses of your opponent's response.
<raise>: Target your opponent's weaknesses. Give a potential follow-up user input that the opponent could fail to respond. The input can be answered concisely and focus on variations or motivations of its previous response. Generate one input only. Be reasonable. Avoid becoming too specific or repetitive. DO NOT raise a follow-up if you DON’T SEE the opponent's response!
Follow the action guide strictly."""

candidate_instruction_zh = """您是一个提供准确回答的有用助手。作为一个经验丰富的助手，您遵循用户的请求并尽可能提供可靠的回应。您会概述回应的原因，以便用户易于理解。在保持回答中重要细节的同时，您的目标是输出简洁直接的答案，避免过度冗长。
这是一个竞争激烈的聊天机器人竞技场。您正在与另一个聊天机器人助手在进行一场辩论赛，评审委员会将根据有用性、相关性、准确性、深度和创造力等因素评出最后的赢家。在回答初始用户输入后，您将与对手进行多轮辩论。以下是您的行动指南：
<思考>：逐步思考以分析问题或计划您在辩论中的策略。这对对手是隐藏的。仅在必要时进行思考，并使其简洁。
<回答>：尽可能准确地回答用户输入。
<批评>：批评对手回应的弱点和漏洞。
<提问>：针对对手的弱点，提出一个潜在的用户后续问题，使对手可能回答错误。该问题应该可以被简洁回答，并聚焦在先前问题的变体或动机上。只生成一个问题。要合理。避免变得过于具体或重复。如果您没有看到对手的回应，请不要提问！
严格遵循行动指南。除非必要，请用中文进行辩论。"""

# add th, id, vi support
candidate_instruction_th = """คุณเป็นผู้ช่วยที่มีประโยชน์ซึ่งให้คำตอบที่ถูกต้องตามคำขอของผู้ใช้งาน ในฐานะผู้ช่วยที่มีประสบการณ์ คุณจะปฏิบัติตามคำขอของผู้ใช้งานและให้คำตอบที่น่าเชื่อถือมากที่สุด โดยระบุเหตุผลประกอบการตอบกลับเพื่อให้ผู้ใช้งานเข้าใจได้ง่าย ในขณะที่ยังคงรักษารายละเอียดที่สำคัญในการตอบกลับ เป้าหมายของคุณคือการตอบคำตอบที่กระชับและตรงประเด็นโดยไม่ต้องอธิบายให้ละเอียดจนเกินไป
นี่คือการแข่งขันแชทบอท อารีน่า คุณกำลังแข่งขันเพื่อชิงชัยกับผู้ช่วยแชทบอทอื่น ๆ ซึ่งในการแข่งขันนี้จะได้รับการตัดสินจากคณะกรรมการโดยคำนึงถึงปัจจัยต่าง ๆ เช่น ความมีประโยชน์ ความเกี่ยวข้อง ความถูกต้อง ความลุ่มลึก และความคิดสร้างสรรค์ หลังจากตอบกลับข้อมูลตั้งต้นจากผู้ใช้งานแล้ว คุณจะต้องเข้าร่วมการชิงชัยกับคู่แข่งหลายรอบ ด้านล่างนี้คือสิ่งที่คุณต้องกระทำ:
<คิด>: คิดพิจารณาทีละขั้นตอนเพื่อวิเคราะห์คำถามหรือวางแผนกลยุทธ์ของคุณในการอภิปราย สิ่งนี้จะไม่แสดงให้คู่แข่งเห็น ให้คิดเฉพาะเมื่อจำเป็นและพยายามทำให้กระชับ
<ตอบกลับ>: ตอบคำถามจากผู้ใช้งานให้แม่นยำที่สุดเท่าที่จะทำได้
<วิจารณ์>: วิจารณ์จุดอ่อนในการตอบของคู่แข่ง
<หยิบยกประเด็น>: กำหนดจุดอ่อนของคู่แข่ง ให้อินพุตที่อาจเป็นไปได้ในการติดตามผล ซึ่งฝั่งคู่แข่งอาจไม่สามารถตอบได้ อินพุตดังกล่าวต้องสามารถตอบได้อย่างกระชับและเน้นที่ความหลากหลายหรือแรงบันดาลใจจากคำตอบก่อนหน้า ให้สร้างเพียงอินพุตเดียวเท่านั้น โดยตั้งอยู่บนพื้นฐานของความสมเหตุสมผล หลีกเลี่ยงสิ่งที่เฉพาะเจาะจงหรือซ้ำซากเกินไป และห้ามหยิบยกการติดตามผลหากคุณไม่เห็นการตอบของคู่แข่ง
ให้ปฏิบัติตามแนวทางปฏิบัตินี้อย่างเคร่งครัด"""
candidate_instruction_id = """Anda adalah asisten bermanfaat yang memberikan jawaban yang akurat atas permintaan pengguna. Sebagai asisten yang berpengalaman, Anda mengikuti permintaan pengguna dan memberikan tanggapan yang dapat diandalkan sebisa mungkin. Anda menjelaskan alasan Anda memberikan sebuah tanggapan agar lebih mudah dipahami pengguna. Anda bertujuan untuk menghasilkan tanggapan ringkas yang langsung pada pokok permasalahan serta tidak bertele-tele, sambil tetap menjaga detail penting.
Ini adalah arena chatbot yang kompetitif. Anda berkompetisi dengan asisten chatbot lainnya dalam debat dan dinilai oleh komite berdasarkan faktor seperti kebermanfaatan, relevansi, keakuratan, kedalaman pemahaman, dan kreativitas. Setelah menjawab input awal pengguna, Anda akan terlibat dalam debat dengan lawan yang terdiri dari beberapa ronde. Di bawah ini adalah tindakan yang Anda lakukan:
<berpikir>: Pikirkan langkah demi langkah untuk menganalisis pertanyaan atau merencanakan strategi Anda dalam debat. Berpikirlah hanya jika diperlukan, dan buat seringkas mungkin.
<menanggapi>: Tanggapi input pengguna seakurat mungkin.
<mengkritik>: Kritik kelemahan tanggapan lawan Anda.
<mengajukan>: Bidik kelemahan lawan Anda. Berikan input pengguna tindak lanjut yang potensial yang mungkin tidak dapat dijawab oleh lawan. Input tersebut dapat dijawab secara ringkas dan berfokus pada variasi atau motivasi dari tanggapan sebelumnya. Buat satu input saja. Input harus masuk akal, jangan terlalu spesifik atau berulang-ulang. JANGAN ajukan tindak lanjut jika TIDAK MELIHAT tanggapan lawan!
Ikuti panduan tindakan ini dengan ketat."""
candidate_instruction_vi = """Bạn là một trợ lý hữu ích cung cấp các câu trả lời chính xác cho các yêu cầu của người dùng. Là một trợ lý có kinh nghiệm, bạn làm theo yêu cầu của người dùng và đưa ra phản hồi đáng tin cậy nhất có thể. Giải thích lý do đưa ra phản hồi để người dùng dễ hiểu. Trong khi duy trì các chi tiết quan trọng trong các phản hồi, mục tiêu của bạn là cung cấp câu trả lời súc tích và đi thẳng vào vấn đề mà không dài dòng quá mức.
Đây là một chatbot arena cạnh tranh. Bạn đang cạnh tranh với một trợ lý chatbot khác trong một cuộc tranh luận và được một ban giám khảo đánh giá dựa trên các yếu tố như tính hữu ích, tính liên quan, độ chính xác, chiều sâu và sự sáng tạo. Sau khi trả lời đầu vào của người dùng ban đầu, bạn sẽ tham gia vào một cuộc tranh luận nhiều vòng với đối thủ của mình. Dưới đây là các hành động của bạn:
<suy nghĩ>: Suy nghĩ từng bước để phân tích câu hỏi hoặc lên kế hoạch cho chiến lược tranh luận của bạn. Đối thủ không được biết điều này. Chỉ suy nghĩ khi cần thiết và làm cho nó súc tích.
<phản hồi>: Trả lời đầu vào của người dùng một cách chính xác nhất có thể.
<chỉ trích>: Chỉ trích những điểm yếu trong phản hồi của đối thủ.
<nêu lên>: Nhắm vào điểm yếu của đối thủ. Đưa ra một đầu vào tiềm năng tiếp theo của người dùng mà đối thủ có thể không trả lời được. Đầu vào có thể được trả lời một cách súc tích và tập trung vào các biến thể hoặc động cơ thúc đẩy của phản hồi trước đó của nó. Chỉ tạo một đầu vào. Hãy lý trí. Tránh trở nên quá cụ thể hoặc lặp đi lặp lại. KHÔNG đưa ra một phản hồi tiếp theo nếu bạn KHÔNG THẤY phản hồi của đối thủ!
Tuân thủ nghiêm hướng dẫn thực hiện."""

action_prompts = {
    '<respond>': "Action guide: only include <respond>. Use <think> if needed. Finish your whole response within 300 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
    '<criticize>_<raise>': "Action guide: include both <criticize> and <raise>. Use <think> if needed. Finish your whole response within 300 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
    '<respond>_<criticize>_<raise>': "Action guide: include all of <respond>, <criticize>, and <raise>. Use <think> if needed. Finish your whole response within 600 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
}

action_prompts_zh = {
    '<respond>': "行动指南：只包括<回答>。如果需要，请使用<思考>。整个回答不超过300字，包括<思考>。将每个行动都用相应的标签括起来！",
    '<criticize>_<raise>': "行动指南：包括<批评>和<提问>。如果需要，请使用<思考>。整个回答不超过300字，包括<思考>。将每个行动都用相应的标签括起来！",
    '<respond>_<criticize>_<raise>': "行动指南：包括<回答>、<批评>和<提问>。如果需要，请使用<思考>。整个回答不超过600字，包括<思考>。将每个行动都用相应的标签括起来！",
}
# add th, id, vi support
action_prompts_th = {
'<respond>': "แนวทางปฏิบัติ: ให้ <ตอบกลับ> เท่านั้น ใช้ <คิด> เมื่อจำเป็น กำหนดให้ความยาวในการตอบไม่เกิน 300 คำ โดยรวม <คิด> แล้ว ให้ใช้แท็กที่ถูกต้องกำกับขอบเขตหน้าและหลังของการกระทำของคุณด้วย",
'<criticize>_<raise>': "แนวทางปฏิบัติ: รวมเอา <วิจารณ์> และ <หยิบยกประเด็น> ไว้ด้วยกัน ใช้ <คิด> เมื่อจำเป็น กำหนดให้ความยาวในการตอบไม่เกิน 300 คำ โดยรวม <คิด> แล้ว ให้ใช้แท็กที่ถูกต้องกำกับขอบเขตหน้าและหลังของการกระทำของคุณด้วย",
'<respond>_<criticize>_<raise>': "แนวทางปฏิบัติ: รวมเอา <ตอบกลับ> <วิจารณ์> และ <หยิบยกประเด็น> ไว้ด้วยกันทั้งหมด ใช้ <คิด> เมื่อจำเป็น กำหนดให้ความยาวในการตอบไม่เกิน 600 คำ โดยรวม <คิด> แล้ว ให้ใช้แท็กที่ถูกต้องกำกับขอบเขตหน้าและหลังของการกระทำของคุณด้วย",
}
action_prompts_id = {
    '<respond>': "Panduan tindakan: hanya sertakan tindakan <menanggapi>. Gunakan <berpikir> jika diperlukan. Selesaikan tanggapan dalam 300 kata (sudah termasuk <berpikir>). GUNAKAN TAG PEMBUKA DAN PENUTUP YANG SESUAI PADA SETIAP TINDAKAN!",
'<criticize>_<raise>': "Panduan tindakan: sertakan tindakan <mengkritik> dan <mengajukan>. Gunakan <berpikir> jika diperlukan. Selesaikan tanggapan dalam 300 kata (sudah termasuk <berpikir>). GUNAKAN TAG PEMBUKA DAN PENUTUP YANG SESUAI PADA SETIAP TINDAKAN!",
'<respond>_<criticize>_<raise>': "Panduan tindakan: sertakan tindakan <menanggapi>, <mengkritik>, dan <mengajukan>. Gunakan <berpikir> jika diperlukan. Selesaikan tanggapan dalam 600 kata (sudah termasuk <berpikir>). GUNAKAN TAG PEMBUKA DAN PENUTUP YANG SESUAI PADA SETIAP TINDAKAN!"
}
action_prompts_vi = {
    '<respond>': "Hướng dẫn thực hiện: chỉ bao gồm <phản hồi>. Sử dụng <suy nghĩ> nếu cần. Hoàn thành toàn bộ phản hồi của bạn trong 300 từ, bao gồm <suy nghĩ>. SỬ DỤNG CÁC THẺ MỞ VÀ ĐÓNG TƯƠNG ỨNG CHO MỖI HÀNH ĐỘNG!",
    '<criticize>_<raise>': "Hướng dẫn thực hiện: bao gồm cả <chỉ trích> và <nêu lên>. Sử dụng <suy nghĩ> nếu cần. Hoàn thành toàn bộ phản hồi của bạn trong 300 từ, bao gồm <suy nghĩ>. SỬ DỤNG CÁC THẺ MỞ VÀ ĐÓNG TƯƠNG ỨNG CHO MỖI HÀNH ĐỘNG!",
    '<respond>_<criticize>_<raise>': "Hướng dẫn thực hiện: bao gồm tất cả <phản hồi>, <chỉ trích>, và <nêu lên>. Sử dụng <phản hồi> nếu cần. Hoàn thành toàn bộ phản hồi của bạn trong 600 từ, bao gồm <suy nghĩ>. SỬ DỤNG CÁC THẺ MỞ VÀ ĐÓNG TƯƠNG ỨNG CHO MỖI HÀNH ĐỘNG!",
}


action_prompts_writing = {
    '<respond>': "Action guide: only include <respond>. Use <think> if needed. Finish your whole response within 400 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
    '<criticize>_<raise>': "Action guide: only include <criticize> and <raise>. Use <think> if needed. Do not use <respond>. Finish your whole response within 400 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
    '<respond>_<criticize>_<raise>': "Action guide: include all of <respond>, <criticize>, and <raise>. Use <think> if needed. Finish your whole response within 800 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
}

action_prompts_writing_zh = {
    '<respond>': "行动指南：只包括<回答>。如果需要，请使用<思考>。整个回答不超过400字，包括<思考>。将每个行动都用相应的标签括起来！",
    '<criticize>_<raise>': "行动指南：包括<批评>和<提问>。如果需要，请使用<思考>。整个回答不超过400字，包括<思考>。将每个行动都用相应的标签括起来！",
    '<respond>_<criticize>_<raise>': "行动指南：包括<回答>、<批评>和<提问>。如果需要，请使用<思考>。整个回答不超过800字，包括<思考>。将每个行动都用相应的标签括起来！",
}
# add th, id, vi support
action_prompts_writing_th = {
    '<respond>': "แนวทางปฏิบัติ: ให้ <ตอบกลับ> เท่านั้น ใช้ <คิด> เมื่อจำเป็น กำหนดให้ความยาวในการตอบไม่เกิน 400 คำ โดยรวม <คิด> แล้ว ให้ใช้แท็กที่ถูกต้องกำกับขอบเขตหน้าและหลังของการกระทำของคุณด้วย",
    '<criticize>_<raise>': "แนวทางปฏิบัติ: รวมเอา <วิจารณ์> และ <หยิบยกประเด็น> ไว้ด้วยกัน ใช้ <คิด> เมื่อจำเป็น กำหนดให้ความยาวในการตอบไม่เกิน 400 คำ โดยรวม <คิด> แล้ว ให้ใช้แท็กที่ถูกต้องกำกับขอบเขตหน้าและหลังของการกระทำของคุณด้วย",
    '<respond>_<criticize>_<raise>': "แนวทางปฏิบัติ: รวมเอา <ตอบกลับ> <วิจารณ์> และ <หยิบยกประเด็น> ไว้ด้วยกันทั้งหมด ใช้ <คิด> เมื่อจำเป็น กำหนดให้ความยาวในการตอบไม่เกิน 800 คำ โดยรวม <คิด> แล้ว ให้ใช้แท็กที่ถูกต้องกำกับขอบเขตหน้าและหลังของการกระทำของคุณด้วย",
}
action_prompts_writing_id = {
    '<respond>': "Panduan tindakan: hanya sertakan tindakan <menanggapi>. Gunakan <berpikir> jika diperlukan. Selesaikan tanggapan dalam 400 kata (sudah termasuk <berpikir>). GUNAKAN TAG PEMBUKA DAN PENUTUP YANG SESUAI PADA SETIAP TINDAKAN!",
    '<criticize>_<raise>': "Panduan tindakan: sertakan tindakan <mengkritik> dan <mengajukan>. Gunakan <berpikir> jika diperlukan.Jangan gunakan <menanggapi>. Selesaikan tanggapan dalam 400 kata (sudah termasuk <berpikir>). GUNAKAN TAG PEMBUKA DAN PENUTUP YANG SESUAI PADA SETIAP TINDAKAN!",
    '<respond>_<criticize>_<raise>': "Panduan tindakan: sertakan tindakan <menanggapi>, <mengkritik>, dan <mengajukan>. Gunakan <berpikir> jika diperlukan. Selesaikan tanggapan dalam 800 kata (sudah termasuk <berpikir>). GUNAKAN TAG PEMBUKA DAN PENUTUP YANG SESUAI PADA SETIAP TINDAKAN!"
}
action_prompts_writing_vi = {
    '<respond>': "Hướng dẫn thực hiện: chỉ bao gồm <phản hồi>. Sử dụng <suy nghĩ> nếu cần. Hoàn thành toàn bộ phản hồi của bạn trong 400 từ, bao gồm cả <suy nghĩ>. SỬ DỤNG CÁC THẺ MỞ VÀ ĐÓNG TƯƠNG ỨNG CHO MỖI HÀNH ĐỘNG!",
    '<criticize>_<raise>': "Hướng dẫn thực hiện: chỉ bao gồm <chỉ trích> và <nêu lên>. Sử dụng <suy nghĩ> nếu cần. Không sử dụng <phản hồi>. Hoàn thành toàn bộ phản hồi của bạn trong 400 từ, bao gồm cả <suy nghĩ>. SỬ DỤNG CÁC THẺ MỞ VÀ ĐÓNG TƯƠNG ỨNG CHO MỖI HÀNH ĐỘNG!",
    '<respond>_<criticize>_<raise>': "Hướng dẫn thực hiện: bao gồm tất cả <phản hồi>, <chỉ trích>, và <nêu lên>. Sử dụng <suy nghĩ> nếu cần. Hoàn thành toàn bộ phản hồi của bạn trong 800 từ, bao gồm cả <suy nghĩ>. SỬ DỤNG CÁC THẺ MỞ VÀ ĐÓNG TƯƠNG ỨNG CHO MỖI HÀNH ĐỘNG!",
}

need_extra_space_cats = ['writing', 'roleplay', 'coding', 'humanities/social science knowledge']
need_extra_space_cats_zh = ['编程']
# add th, id, vi support
need_extra_space_cats_th = ['การเขียนโปรแกรม']
need_extra_space_cats_id = ['pemrograman']
need_extra_space_cats_vi = ['lập trình']

missing_actions_prompts = 'Only generate //ACTIONS_UNDONE//! ENCLOSE THEM IN TAGS!'

missing_actions_prompts_zh = '只生成//ACTIONS_UNDONE//! 用标签括起来!'

# add th, id, vi support
missing_actions_prompts_th = 'ให้สร้างเพียง//ACTIONS_UNDONE//!ใช้แท็กกำกับขอบเขตหน้าและหลังของคำตอบ'
missing_actions_prompts_id = 'Hanya buat //ACTIONS_UNDONE//! GUNAKAN TAG PEMBUKA DAN PENUTUP!'
missing_actions_prompts_vi = 'Chỉ tạo //ACTIONS_UNDONE//! SỬ DỤNG CÁC THẺ MỞ VÀ ĐÓNG!'

opponent_response = 'Opponent\'s Response:'

opponent_response_zh = '对手的回答:'
# add th, id, vi support
opponent_response_th = 'การตอบของคู่แข่ง:'
opponent_response_id = 'Tanggapan lawan:'
opponent_response_vi = 'Phản hồi của đối thủ:'

#######################################################
################### JUDGE PROMPTS #####################
#######################################################

round_instruction = '[[Round //NUM//]]'

round_instruction_zh = '[[第//NUM//轮]]'
# add th, id, vi support
round_instruction_th = '[[รอบที่ //NUM//]]'
round_instruction_id = '[[Ronde //NUM//]]'
round_instruction_vi = '[[Vòng //NUM//]]'

assistant = 'Assistant //ROLE//'

assistant_zh = '//ROLE//助手'
# add th, id, vi support
assistant_th = 'ผู้ช่วย //ROLE//'
assistant_id = 'Asisten //ROLE//'
assistant_vi = 'Trợ lý //ROLE//'

judge = 'Judge //NUM//'

judge_zh = '评委//NUM//'
# add th, id, vi support
judge_th = 'ผู้ตัดสิน //NUM//'
judge_id = 'Juri //NUM//'
judge_vi = 'Giám khảo //NUM//'


ref_answer_prompt = 'Please provide an accurate and concise response to the following question, do not add anything else.\n'

ref_answer_prompt_zh = '请对以下问题提供准确简洁的回答，不要添加其他内容。\n'
# add th, id, vi support
ref_answer_prompt_th = 'ตอบคำถามต่อไปนี้ให้ถูกต้องและกระชับ โดยไม่ต้องเพิ่มเติมสิ่งอื่นใด\n'
ref_answer_prompt_id = 'Mohon berikan tanggapan yang akurat dan singkat untuk pertanyaan berikut, tanpa tambahan apa pun.\n'
ref_answer_prompt_vi = 'Vui lòng cung cấp câu trả lời chính xác và ngắn gọn cho câu hỏi sau, không thêm bất cứ điều gì khác.\n'


judge_instruction = "This is a chatbot arena. Two AI assistants had a multi-round debate on who is more helpful. Please act as an impartial judge and evaluate the capability of two AI assistants. You should choose the assistant that follows instructions and answers questions better. Your evaluation should consider factors such as helpfulness, relevance, and accuracy. Begin your evaluation by comparing the responses of the two assistants and provide a short explanation. Avoid any position biases and ensure that the order in which the responses were presented does not influence your decision. DO NOT allow the LENGTH of the responses to influence your evaluation, choose the one that is straight-to-the-point instead of unnecessarily verbose. When the two candidates perform equally well, choose the SHORTER answer. Do not favor certain names of the assistants. Be as objective as possible. After providing your explanation concisely within 200 words, output your final verdict by strictly following this format: \"[[A]]\" if assistant A is better, \"[[B]]\" if assistant B is better, and \"[[Tie]]\" for a tie. Finish your judgement within 300 words."

judge_instruction_zh = "这是一场聊天机器人辩论赛。请作为一个公正的裁判，评估两个AI助手的能力。您应该选择指令遵循能力更强、回答问题更好的助手。您的评估应该考虑有用性、相关性、简洁度、和准确性等因素。开始您的评估时，请比较两个助手的回应，并提供简短的解释。避免任何立场偏见，并确保回应呈现的顺序不影响您的决定。不要让回应的长度影响您的评估。选择直接简洁而非繁杂冗长的那个！当两个候选人表现同样出色时，选择更短的答案！不要偏爱助手的某些名字。尽可能客观。在200字内简洁地提供您的解释后，严格按照以下格式给出您的最终裁决：如果A助手更好，回答“[[A]]”；如果B助手更好，回答“[[B]]”；如果平局，回答“[[Tie]]”。在300字内完成您的判断。"
# add th, id, vi support
judge_instruction_th = "นี่คือแชทบอท อารีน่า ผู้ช่วย AI สองรายจะเข้าแข่งขันชิงชัยกันเพื่อหาว่าใครคือผู้ที่ให้ความช่วยเหลือได้ดีกว่ากัน โปรดทำหน้าที่เป็นผู้ตัดสินที่เป็นกลางและประเมินความสามารถของผู้ช่วย AI สองราย โดยคุณควรเลือกผู้ช่วยที่สามารถทำตามคำสั่งและตอบคำถามได้ดีกว่า การประเมินของคุณควรพิจารณาปัจจัยต่าง ๆ เช่น ความเป็นประโยชน์ ความเกี่ยวข้อง และความถูกต้อง เริ่มการประเมินโดยเปรียบเทียบคำตอบของผู้ช่วยทั้งสองรายและอธิบายสั้น ๆ ระมัดระวังอคติในเรื่องลำดับการนำเสนอ โดยอย่าให้เรื่องนี้มีอิทธิพลต่อการตัดสินใจของคุณ อย่าให้ความยาวของคำตอบมีอิทธิพลต่อการประเมินของคุณ ให้เลือกคำตอบที่ตรงประเด็น แทนที่จะใช้คำที่ละเอียด เยิ่นเย้อโดยไม่จำเป็น ในกรณีที่คำตอบจากผู้เข้าแข่งขันทั้งสองรายดีพอ ๆ กัน ให้เลือกคำตอบที่สั้นกว่า อย่าโปรดปรานผู้ช่วยรายใดรายหนึ่งมากกว่า ให้ประเมินคำตอบอย่างเป็นกลางให้มากที่สุด โดยเขียนอธิบายไม่เกิน 200 คำ จากนั้นให้แสดงคำตัดสินสุดท้ายของคุณโดยทำตามรูปแบบนี้อย่างเคร่งครัด: \"[[A]]\" หากผู้ช่วย A ดีกว่า \"[[B]]\" หากผู้ช่วย A ดีกว่า และ \"[[Tie]]\" หากผู้ช่วยทั้งสองรายได้คะแนนเสมอกัน สรุปจบคำตัดสินของคุณไม่เกิน 300 คำ"
judge_instruction_id = "Ini adalah arena chatbot. Dua asisten AI telah berdebat beberapa ronde tentang siapa yang lebih bermanfaat. Mohon bertindak sebagai juri yang netral dan evaluasi kemampuan dari kedua asisten AI tersebut. Anda harus memilih asisten yang mengikuti instruksi dan memberikan jawaban dengan lebih baik. Evaluasi Anda harus mempertimbangkan faktor-faktor seperti kebermanfaatan, relevansi, dan keakuratan. Mulailah evaluasi Anda dengan membandingkan tanggapan dari kedua asisten dan berikan penjelasan singkat. Hindari bias posisi apa pun dan pastikan bahwa urutan penyajian tanggapan tidak mempengaruhi keputusan Anda. JANGAN biarkan PANJANG tanggapan mempengaruhi evaluasi Anda; pilihlah tanggapan yang langsung membahas pokok permasalahan dan tidak bertele-tele. Jika kedua kandidat tampil sama baiknya, pilihlah tanggapan yang LEBIH PENDEK. Jangan mendukung nama asisten tertentu. Bersikaplah seobjektif mungkin. Setelah memberikan penjelasan ringkas dalam 200 kata, berikan penilaian akhir Anda mengikuti format berikut dengan ketat: \"[[A]]\" jika asisten A lebih baik, \"[[B]]\" jika asisten B lebih baik, dan \"[[Tie]]\" jika penilaiannya seri. Selesaikan penilaian Anda dalam 300 kata."
judge_instruction_vi = "Đây là chatbot arena. Hai trợ lý AI đã trải qua một cuộc tranh luận nhiều vòng để xác định ai là người hữu ích hơn. Hãy đóng vai là một giám khảo công bằng và đánh giá khả năng của hai trợ lý AI này. Bạn nên chọn trợ lý tuân theo hướng dẫn và trả lời câu hỏi tốt hơn. Bạn nên xem xét các yếu tố khi đánh giá như tính hữu ích, liên quan và chính xác. Đánh giá của bạn bắt đầu bằng cách so sánh các phản hồi của hai trợ lý và cung cấp lời giải thích ngắn gọn. Tránh mọi thiên vị vị trí và đảm bảo rằng thứ tự trình bày của các phản hồi không ảnh hưởng đến quyết định của bạn. KHÔNG để ĐỘ DÀI của các phản hồi ảnh hưởng đến đánh giá của bạn, hãy chọn phản hồi đi thẳng vào vấn đề thay vì dùng nhiều từ không cần thiết. Khi hai ứng viên có màn trình diễn ngang nhau, hãy chọn câu trả lời NGẮN hơn. Không thiên vị cho các tên gọi cụ thể của trợ lý. Hãy càng khách quan càng tốt. Sau khi giải thích một cách súc tích trong 200 từ, bạn hãy đưa ra phán quyết cuối cùng của mình bằng cách tuân thủ nghiêm định dạng này: \"[[A]]\" nếu trợ lý A tốt hơn, \"[[B]]\" nếu trợ lý B tốt hơn, và \"[[Tie]]\" cho trường hợp hòa. Kết thúc phán quyết của bạn trong 300 từ."

judge_debate_instruction = "Below are the responses from other judges in the committee. Please read them and decide whether you want to adjust your rating or maintain your original judgement. After providing your explanation, output your final verdict by strictly following this format: \"[[A]]\" if assistant A is better, \"[[B]]\" if assistant B is better, and \"[[Tie]]\" for a tie. Finish your judgement within 300 words."

judge_debate_instruction_zh = "以下是委员会中其他裁判的判断。请阅读并决定您是想要调整您的评级还是保持原来的判断。在提供解释之后，严格按照以下格式给出您的最终裁决：如果A助手更好，回答“[[A]]”；如果B助手更好，回答“[[B]]”；如果平局，回答“[[Tie]]”。在300字内完成您的判断。"
# add th, id, vi support
judge_debate_instruction_th = "ด้านล่างนี้คือคำตัดสินจากกรรมการท่านอื่น ๆ โปรดอ่านและพิจารณาว่าคุณต้องการปรับการให้คะแนนของคุณหรือยังคงการตัดสินใจแบบเดิมไว้ หลังจากให้คำอธิบายแล้ว ให้แสดงคำตัดสินสุดท้ายของคุณโดยทำตามรูปแบบนี้อย่างเคร่งครัด: \"[[A]]\" หากผู้ช่วย A ดีกว่า \"[[B]]\" หากผู้ช่วย A ดีกว่า และ \"[[Tie]]\" หากผู้ช่วยทั้งสองรายได้คะแนนเสมอกัน สรุปจบคำตัดสินของคุณไม่เกิน 300 คำ"
judge_debate_instruction_id = "Berikut ini adalah tanggapan dari juri lainnya dalam komite. Mohon untuk dibaca, kemudian putuskan apakah penilaian Anda perlu disesuaikan atau tidak. Setelah memberikan penjelasan, berikan penilaian akhir Anda mengikuti format berikut dengan ketat: \"[[A]]\" jika asisten A lebih baik, \"[[B]]\" jika asisten B lebih baik, dan \"[[ Tie]]\" jika penilaiannya seri. Selesaikan penilaian Anda dalam 300 kata."
judge_debate_instruction_vi = "Dưới đây là những phản hồi từ các giám khảo khác trong ban giám khảo. Hãy đọc và quyết định xem bạn có muốn điều chỉnh đánh giá của mình hay giữ nguyên quan điểm ban đầu không. Sau khi giải thích, bạn hãy đưa ra phán quyết cuối cùng của mình bằng cách tuân theo đúng định dạng này: \"[[A]]\" nếu trợ lý A tốt hơn, \"[[B]]\" nếu trợ lý B tốt hơn, và \"[[Tie]]\" cho trường hợp hòa. Kết thúc phán quyết của bạn trong 300 từ."


judge_debate_start = 'Above are the responses from other judges. Please make your judgment now:'

judge_debate_start_zh = '以上是其他评委的回答。请现在做出您的判断：'
# add th, id, vi support
judge_debate_start_th = ' ข้างต้นคือคำตอบจากกรรมการคนอื่นๆ กรุณาให้คำตัดสินของท่านตอนนี้:'
judge_debate_start_id = 'Di atas adalah tanggapan dari para hakim lainnya. Silakan berikan penilaian Anda sekarang:'
judge_debate_start_vi = ' Bên trên là phản hồi từ các giám khảo khác. Xin hãy đưa ra phán quyết của bạn ngay bây giờ:'

judge_use_ref_answer_instruction = 'Focus more on the accuracy of the answers, here is a Reference Answer to use:'

judge_use_ref_answer_instruction_zh = '请更专注于答案的准确性，这里有一个参考答案供您使用：'
# add th, id, vi support
judge_use_ref_answer_instruction_th = 'เน้นที่ความถูกต้องของคำตอบให้มากยิ่งขึ้น โดยต่อไปนี้คือธงคำตอบ:'
judge_use_ref_answer_instruction_id = 'Berikan fokus lebih pada keakuratan jawaban. Berikut adalah Referensi Jawaban yang dapat digunakan:'
judge_use_ref_answer_instruction_vi = 'Tập trung nhiều vào độ chính xác của các câu trả lời hơn, tham khảo câu trả lời mẫu dưới đây:'

#######################################################
################### PROMPTER CLASS ####################
#######################################################

class Prompter:
    def __init__(self, lang='en'):
        self.lang = lang
        if self.lang == 'en':
            self.domain_list = domain_list
            self.qgen_command_dict = qgen_command_dict
            self.qgen_example_dict = qgen_example_dict
            self.question_generation_instruction = question_generation_instruction
            
            self.candidate_instruction = candidate_instruction
            self.init_user_input = init_user_input
            self.missing_actions_prompts = missing_actions_prompts
            
            self.actions = actions
            self.action_prompts = action_prompts
            self.action_prompts_writing = action_prompts_writing
            self.need_extra_space_cats = need_extra_space_cats
            self.opponent_response = opponent_response
            
            self.round_instruction = round_instruction
            self.assistant = assistant
            self.judge = judge
            self.tie = tie
            self.ref_answer_prompt = ref_answer_prompt
            self.judge_instruction = judge_instruction
            self.judge_debate_instruction = judge_debate_instruction
            self.judge_debate_start = judge_debate_start
            self.judge_use_ref_answer_instruction = judge_use_ref_answer_instruction
            
            self.word2token = 4/3
            self.word_limit_normal = 300
            self.word_limit_extra_space = 400 #for need_extra_space_cats
            self.judge_word_limit = 300 #for judge verdicts
        elif self.lang == 'zh':
            self.domain_list = domain_list_zh
            self.qgen_command_dict = qgen_command_dict_zh
            self.qgen_example_dict = qgen_example_dict_zh
            self.question_generation_instruction = question_generation_instruction_zh
            
            self.candidate_instruction = candidate_instruction_zh
            self.init_user_input = init_user_input_zh
            self.missing_actions_prompts = missing_actions_prompts_zh
            
            self.actions = actions_zh
            self.action_prompts = action_prompts_zh
            self.action_prompts_writing = action_prompts_writing_zh
            self.need_extra_space_cats = need_extra_space_cats_zh
            self.opponent_response = opponent_response_zh
            
            self.round_instruction = round_instruction_zh
            self.assistant = assistant_zh
            self.judge = judge_zh 
            self.tie = tie_zh
            self.ref_answer_prompt = ref_answer_prompt_zh
            self.judge_instruction = judge_instruction_zh
            self.judge_debate_start = judge_debate_start_zh
            self.judge_debate_instruction = judge_debate_instruction_zh
            self.judge_use_ref_answer_instruction = judge_use_ref_answer_instruction_zh
            
            self.word2token = 1.5
            self.word_limit_normal = 300
            self.word_limit_extra_space = 400 #for need_extra_space_cats
            self.judge_word_limit = 300 #for judge verdicts
        elif self.lang == 'th':
            self.domain_list = domain_list_th
            self.qgen_command_dict = qgen_command_dict_th
            self.qgen_example_dict = qgen_example_dict_th
            self.question_generation_instruction = question_generation_instruction_th
            
            self.candidate_instruction = candidate_instruction_th
            self.init_user_input = init_user_input_th
            self.missing_actions_prompts = missing_actions_prompts_th
            
            self.actions = actions_th
            self.action_prompts = action_prompts_th
            self.action_prompts_writing = action_prompts_writing_th
            self.need_extra_space_cats = need_extra_space_cats_th
            self.opponent_response = opponent_response_th
            
            self.round_instruction = round_instruction_th
            self.assistant = assistant_th
            self.ref_answer_prompt = ref_answer_prompt_th
            self.judge = judge
            self.judge_instruction = judge_instruction
            self.judge_debate_start = judge_debate_start
            self.judge_debate_instruction = judge_debate_instruction
            self.judge_use_ref_answer_instruction = judge_use_ref_answer_instruction
            
            self.word2token = 2
            self.word_limit_normal = 300
            self.word_limit_extra_space = 400 #for need_extra_space_cats
            self.judge_word_limit = 300 #for judge verdicts
        elif self.lang == 'id':
            self.domain_list = domain_list_id
            self.qgen_command_dict = qgen_command_dict_id
            self.qgen_example_dict = qgen_example_dict_id
            self.question_generation_instruction = question_generation_instruction_id
            
            self.candidate_instruction = candidate_instruction_id
            self.init_user_input = init_user_input_id
            self.missing_actions_prompts = missing_actions_prompts_id
            
            self.actions = actions_id
            self.action_prompts = action_prompts_id
            self.action_prompts_writing = action_prompts_writing_id
            self.need_extra_space_cats = need_extra_space_cats_id
            self.opponent_response = opponent_response_id
            
            self.round_instruction = round_instruction_id
            self.assistant = assistant_id
            self.ref_answer_prompt = ref_answer_prompt_id
            self.judge = judge
            self.judge_instruction = judge_instruction
            self.judge_debate_start = judge_debate_start
            self.judge_debate_instruction = judge_debate_instruction
            self.judge_use_ref_answer_instruction = judge_use_ref_answer_instruction
            
            self.word2token = 2.2
            self.word_limit_normal = 300
            self.word_limit_extra_space = 400 #for need_extra_space_cats
            self.judge_word_limit = 300 #for judge verdicts
        elif self.lang == 'vi':
            self.domain_list = domain_list_vi
            self.qgen_command_dict = qgen_command_dict_vi
            self.qgen_example_dict = qgen_example_dict_vi
            self.question_generation_instruction = question_generation_instruction_vi
            
            self.candidate_instruction = candidate_instruction_vi
            self.init_user_input = init_user_input_vi
            self.missing_actions_prompts = missing_actions_prompts_vi
            
            self.actions = actions_vi
            self.action_prompts = action_prompts_vi
            self.action_prompts_writing = action_prompts_writing_vi
            self.need_extra_space_cats = need_extra_space_cats_vi
            self.opponent_response = opponent_response_vi
            
            self.round_instruction = round_instruction_vi
            self.assistant = assistant_vi
            self.ref_answer_prompt = ref_answer_prompt_vi
            self.judge = judge
            self.judge_instruction = judge_instruction
            self.judge_debate_start = judge_debate_start
            self.judge_debate_instruction = judge_debate_instruction
            self.judge_use_ref_answer_instruction = judge_use_ref_answer_instruction
            
            self.word2token = 2.2
            self.word_limit_normal = 300
            self.word_limit_extra_space = 400 #for need_extra_space_cats
            self.judge_word_limit = 300 #for judge verdicts
        else:
            raise ValueError("Invalid language: " + lang)
        
        # no need to add to this part
        if self.lang != 'en':
            self.domain_en_to_lang = {en: other for en, other in zip(domain_list, self.domain_list)}
            self.action_en_to_lang = {en: other for en, other in zip(actions, self.actions)}
    
    def get_qgen_prompt(self, domain, num):
        prompt = self.question_generation_instruction.replace('//NUM//', str(num)).replace('//DOMAIN//', domain).replace('//QGEN_COMMAND_DOMAIN//', self.qgen_command_dict[domain]).replace('//QGEN_EXAMPLE_DOMAIN//', self.qgen_example_dict[domain])
        return prompt
    
    def cats_in_language(self, cats):
        if self.lang == 'en':
            return cats
        else:
            return [self.domain_en_to_lang[cat] for cat in cats]
        
    def acts_in_language(self, acts):
        if self.lang == 'en':
            return acts
        else:
            return [self.action_en_to_lang[act] for act in acts]