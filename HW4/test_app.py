import unittest
import app as todo_app # 2차시에 친 app.py 를 가져온다


class TodoApiTest(unittest.TestCase):

    def setUp(self): # 테스트 하나마다 먼저 돈다
        todo_app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        todo_app.app.config["TESTING"] = True
        self.client = todo_app.app.test_client()
        self.ctx = todo_app.app.app_context()
        self.ctx.push()
        todo_app.db.drop_all()
        todo_app.db.create_all()

    def tearDown(self): # 끝날 때마다 돈다
        todo_app.db.session.remove()
        self.ctx.pop()

    def test_만든_것이_목록에_그대로_나온다(self):
        self.client.post("/api/todos/", json={"text": "우유 사기", "done": True})
        self.client.post("/api/todos/", json={"text": "책 반납"})
        r = self.client.get("/api/todos/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json()), 2) # 둘 다 나와야 한다

    def test_만들면_201_과_만들어진_것이_온다(self):
        r = self.client.post("/api/todos/", json={"text": "우유 사기"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["text"], "우유 사기")

    def test_없는_번호는_404_다(self):
        r = self.client.get("/api/todos/999")
        self.assertEqual(r.status_code, 404)

    def test_patch_는_보낸_칸만_바꾼다(self):
        made = self.client.post("/api/todos/", json={"text": "책 반납"}).get_json()
        r = self.client.patch(f"/api/todos/{made['id']}", json={"done": True})
        self.assertEqual(r.get_json()["text"], "책 반납") # 글자는 그대로
        self.assertTrue(r.get_json()["done"]) # 완료만 바뀜

    def test_지우면_204_고_다시_찾으면_404_다(self):
        made = self.client.post("/api/todos/", json={"text": "지울 것"}).get_json()
        self.assertEqual(self.client.delete(f"/api/todos/{made['id']}").status_code, 204)
        self.assertEqual(self.client.get(f"/api/todos/{made['id']}").status_code, 404)

    def test_done_true면_완료된_것만_나온다(self):
        self.client.post(
            "/api/todos/",
            json={"text": "과제", "done": True}
        )
        self.client.post(
            "/api/todos/",
            json={"text": "공부", "done": False}
        )

        r = self.client.get("/api/todos/?done=true")

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json()), 1)
        self.assertEqual(r.get_json()[0]["text"], "과제")

    def test_put으로_할_일을_수정한다(self):
        made = self.client.post(
            "/api/todos/",
            json={"text": "기존 할 일"}
        ).get_json()

        r = self.client.put(
            f"/api/todos/{made['id']}",
            json={
                "text": "수정된 할 일",
                "done": True,
                "note": "수정한 설명"
            }
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["text"], "수정된 할 일")
        self.assertTrue(r.get_json()["done"])

    def test_note가_저장된다(self):
        r = self.client.post(
            "/api/todos/",
            json={
                "text": "우유 사기",
                "note": "2리터짜리"
            }
        )

        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["note"], "2리터짜리")

    def test_patch로_note만_수정한다(self):
        made = self.client.post(
            "/api/todos/",
            json={
                "text": "책 반납",
                "note": "도서관"
            }
        ).get_json()

        r = self.client.patch(
            f"/api/todos/{made['id']}",
            json={"note": "학교 도서관"}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["text"], "책 반납")
        self.assertEqual(r.get_json()["note"], "학교 도서관")

    def test_done_false면_미완료만_나온다(self):
        self.client.post(
            "/api/todos/",
            json={"text": "완료", "done": True}
        )
        self.client.post(
            "/api/todos/",
            json={"text": "미완료", "done": False}
        )

        r = self.client.get("/api/todos/?done=false")

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json()), 1)
        self.assertEqual(r.get_json()[0]["text"], "미완료")
