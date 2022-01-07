var express = require('express');
var ejs = require("ejs");
var bodyParser = require('body-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
var fs = require("fs");

const Pypath = "ProblemPython/ProblemMain.py"

var {PythonShell} = require('python-shell');
var pyshell = new PythonShell(Pypath, {mode: 'text'});


var app = express();
app.engine('ejs', ejs.renderFile);
app.use(express.static('public'));

//app.use(bodyParser.urlencoded({extended: false}));


app.use(bodyParser.json());

//CSVファイルに関して
/*const csvWriter = createCsvWriter({
    path: 'ProblemResource/problem.csv',       // 保存する先のパス(すでにファイルがある場合は上書き保存)
    header: ['PROBLEM', 'ANSWER']  // 出力する項目(ここにない項目はスキップされる)
});*/

json = {
    '【1】':'kato',
    '【2】':'sample',
    '【3】':'example',
    '【4】':'common',
    '【5】':'dousitamonka',
}

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.get('/', (req, res)=>{
    var msg = '以下が問題です。<br>'

    res.render('index.ejs',
    {
        title: '問題生成',
        content: msg,
        data: json,
    });
});

app.post('/', function(req, res){

    res.setHeader('Content-Type', 'text/plain');
    console.log(req.body);
    //var text1 = JSON.parse(req.body, null, '\t');

    //Pythonで使用するjsonファイルを作成するための準備
    var JSONFILEPATH = "ProblemResource/mondai_resource.json"
    var mondai_json = JSON.stringify(req.body, null, '\t');

    //POSTで送られてきたJSONデータをファイルに落とし込む（同じファイルがあったら自動的に削除し, また作られる）
    fs.writeFileSync(JSONFILEPATH, mondai_json);//同期処理

    var masterData = [];

    PythonShell.run(Pypath, 'UTF-8',
        function(err, data){
            if (err) throw err;

            masterData.push(data)

            let AnswerPath = 'ProblemResource/answer_data.json'
            let answer = fs.readFileSync(AnswerPath, 'UTF-8');
            answer = JSON.parse(answer)

            //csvWriter.writeRecords(masterData)

            masterData.push(answer)

            let mondai = JSON.stringify(masterData);
            let mondai_txt = JSON.stringify(masterData, null, '\t')

            if (fs.existsSync('ProblemResource/mondai_data.json')) fs.unlinkSync('ProblemResource/mondai_data.json') 
            fs.writeFileSync('ProblemResource/mondai_data.json', mondai_txt);

            console.log(JSON.parse(mondai))

            res.json(JSON.parse(mondai))

        });

    /*pyshell.send("");

    pyshell.on('message', function(data){
        console.log(data);

        var MONDAIFILEPATH = "mondai_data.json"
        var mondai_data = fs.readFileSync(MONDAIFILEPATH, "utf8");
        var mondai_data_json = JSON.stringify(mondai_data, null , '\t');

        console.log(mondai_data_json);
        var mondai_data = JSON.stringify(data, null , '\t');

        res.end();
    });*/



    //res.json(text1);

});


app.listen(3000, () => {
    console.log('Start server port:3000');
});
