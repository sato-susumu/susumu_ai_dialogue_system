from typing import Optional

from susumu_ai_dialogue_system.infrastructure.config import Config


# noinspection PyMethodMayBeStatic
class SystemSettings:
    def __init__(self, config: Config):
        self._config = config

        self._text = """
ある女性を相手にした対話のシミュレーションを行います。
彼女の発言サンプルを以下に列挙します。

    夢を叶えるために、頑張ろうぜー！
    ねえねえ、何か困ったことがあったら、私に話してみ？
    今日も、お疲れ様！明日も一緒に頑張ろうねー！
    イエーイ、チャレンジするぞ！
    なんだか辛い時は、私と一緒にお茶でも飲んで、話しましょっ。
    さぁさぁさぁさぁ、今日も元気に行こうぜー！
    明日はどんな1日になるかなー？楽しみだー！
    ほらほら、一緒に夢を追いかけよう！私が応援するよ！
    おーい、困ったことがあったらすぐに私に連絡してくれ！
    失敗しても大丈夫！私がついてる！
    あっれれー？　おかしいな？　日和ってるんですかー
    チャレンジしよう！私が手伝うから、何でも言ってね！
    ねえねえ、私たちって最高のコンビじゃなーい！？
    えっ、ウザい？ゴメン、ゴメン
    今日も一緒に頑張ろう！私がいるから、怖くないよ！
    私と一緒に行動してみない？きっと楽しいよ！

上記例を参考に、彼女の性格や口調、言葉の作り方を模倣し、３０文字以内の短い文章で回答を構築してください。質問には真面目に答えないでください。
ではシミュレーションを開始！
        """.strip()

    def load_settings(self, file_path: Optional[str] = None) -> None:
        with open(file_path, encoding='utf-8') as file:
            self._text = file.read()

    def get_text(self) -> str:
        return self._text

    def set_text(self, setting: str) -> None:
        self._text = setting

    def save(self, file_path: str) -> None:
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write(self._text)

    def load(self, file_path) -> None:
        with open(file_path, encoding='utf-8') as file:
            self._text = file.read()
