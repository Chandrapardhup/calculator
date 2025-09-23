from flask import Flask, render_template_string, request, jsonify
import requests, time

app = Flask(__name__)

SERVICE_URLS = {
    "+": "http://addition:5000/add",
    "-": "http://subtraction:5000/subtract",
    "*": "http://multiplication:5000/multiply",
    "/": "http://division:5000/divide"
}

def call_service(op, x, y, retries=5):
    url = SERVICE_URLS.get(op)
    if not url:
        return "Invalid operation"
    for _ in range(retries):
        try:
            r = requests.get(url, params={"x": x, "y": y}, timeout=3)
            return r.json().get("result")
        except:
            time.sleep(1)
    return "Error connecting service"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Interactive Calculator</title>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" rel="stylesheet">
<style>
body { background:#1e1e1e; color:#fff; font-family:'Segoe UI',sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; }
.container { background:#2c2c2c; padding:30px; border-radius:20px; box-shadow:0 0 30px #000; width:380px; display:flex; flex-direction:column; align-items:center; }
input { width:90%; padding:20px; font-size:28px; border:none; border-radius:12px; margin-bottom:20px; background:#1e1e1e; color:#fff; text-align:center; }
button { width:22%; padding:18px; margin:2%; border:none; border-radius:12px; background:#ff9500; color:#fff; font-size:22px; cursor:pointer; transition:0.2s; }
button:hover { background:#ffa733; transform:scale(1.1); }
.row { display:flex; justify-content:space-between; width:100%; }
h2 { text-align:center; margin-bottom:20px; color:#ff9500; }
</style>
</head>
<body>
<div class="container">
<h2><i class="fa-solid fa-calculator"></i> Calculator</h2>
<input type="text" id="display" placeholder="0">
<div class="row">
  <button onclick="press('7')">7</button>
  <button onclick="press('8')">8</button>
  <button onclick="press('9')">9</button>
  <button onclick="press('/')"><i class="fa-solid fa-divide"></i></button>
</div>
<div class="row">
  <button onclick="press('4')">4</button>
  <button onclick="press('5')">5</button>
  <button onclick="press('6')">6</button>
  <button onclick="press('*')"><i class="fa-solid fa-xmark"></i></button>
</div>
<div class="row">
  <button onclick="press('1')">1</button>
  <button onclick="press('2')">2</button>
  <button onclick="press('3')">3</button>
  <button onclick="press('-')"><i class="fa-solid fa-minus"></i></button>
</div>
<div class="row">
  <button onclick="press('0')">0</button>
  <button onclick="press('.')">.</button>
  <button onclick="calculate()"><i class="fa-solid fa-equals"></i></button>
  <button onclick="press('+')"><i class="fa-solid fa-plus"></i></button>
</div>
<div class="row">
  <button onclick="clearDisplay()" style="width:100%; background:#ff3b30;"><i class="fa-solid fa-trash"></i> Clear</button>
</div>
</div>
<script>
let currentInput = "";
let lastResult = null;

document.addEventListener("keydown", function(e){
    if("0123456789.".includes(e.key)){
        // Number or dot
        currentInput += e.key;
        document.getElementById("display").value = currentInput;
    } else if("+-*/".includes(e.key)){
        // Operator
        if(currentInput === "" && lastResult !== null){
            currentInput = lastResult + e.key;
        } else {
            currentInput += e.key;
        }
        document.getElementById("display").value = currentInput;
    } else if(e.key === "Enter"){
        calculate();
    } else if(e.key === "Backspace"){
        currentInput = currentInput.slice(0,-1);
        document.getElementById("display").value = currentInput;
    }
});

function press(val){
    currentInput += val;
    document.getElementById("display").value = currentInput;
}

function clearDisplay(){
    currentInput = "";
    lastResult = null;
    document.getElementById("display").value = "";
}

function calculate(){
    let match = currentInput.match(/(-?[\\d.]+)([+\\-*/])(-?[\\d.]+)/);
    if(!match){
        document.getElementById("display").value = "Invalid";
        currentInput = "";
        return;
    }
    let x = match[1];
    let op = match[2];
    let y = match[3];
    fetch(`/calculate?x=${x}&y=${y}&op=${encodeURIComponent(op)}`)
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("display").value = data.result;
        lastResult = data.result;  // store result for next calculation
        currentInput = "";          // reset input for next number
    });
}

<script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/calculate", methods=["GET"])
def calc():
    x = request.args.get("x", "").strip()
    y = request.args.get("y", "").strip()
    op = request.args.get("op", "").strip()
    try:
        result = call_service(op, float(x), float(y))
    except ValueError:
        result = "Invalid input"
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

