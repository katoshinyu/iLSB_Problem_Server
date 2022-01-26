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

            let ProblemPath = 'ProblemResource/ProblemInformation.json';
            let ProblemJson = fs.readFileSync(ProblemPath, 'UTF-8');
            let ProblemJsonData = JSON.parse(ProblemJson)

            //csvWriter.writeRecords(masterData)

            let ProblemData = JSON.stringify(ProblemJsonData);
            let Problem_txt = JSON.stringify(ProblemData, null, '\t')

            if (fs.existsSync('ProblemResource/mondai_data.json')) fs.unlinkSync('ProblemResource/mondai_data.json') 
            fs.writeFileSync('ProblemResource/mondai_data.json', Problem_txt);

            console.log(masterData)
            console.log(JSON.parse(ProblemData))

            res.json(JSON.parse(ProblemData))

        });
});
app.post('/save', function(req, res){
    
});


app.listen(3000, () => {
    console.log('Start server port:3000');
});
