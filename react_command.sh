npx create-react-app react-frontend --template typescript

npm start

npm run build

npm install ts-loader --save-dev

npx webpack

npm install recharts

※メモ
・Django の方で React 用のファイルは一つ(templates/react-base.html)
    <div id="root"><div>
    <script type="text/javascript" src="{% static 'js/main.cc3edf5b.js' %}"></script>
  この id="root" に対して js/main~.js を読み込んでいて、jsをstatic js を作成するために npm run build が必要
  複数のページを切り替えるためには、React Router を使ってApp.jsx にルーティングを追加
  その後、Django の urls を設定してリンクすることで React のAPP.jsx に設定したルーティングのtsxファイルが表示される。

・React でbuild 後のファイルにはハッシュがつくため毎回変わる
 ->webpack.config.js を作成して npm run build -> npx webpack を実行することで出力するファイル名/場所を変更することが可能
 ->ファイルの拡張子設定注意 resolve: {extensions: ['.js', '.jsx', '.json', '.ts', '.tsx']} ※App.tsx なら .tsx が必要



 # 業種ごとの分析リストの結果の下にAWS BedRockで考察した結果を表示する