from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>🧮 Smart Calculator</title>
<style>
* { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
body {
  display:flex; justify-content:center; align-items:center; height:100vh;
  margin:0; background: radial-gradient(circle at center, #1e1e1e, #0d0d0d); color:white;
}
.calculator {
  width: 340px; border-radius: 20px; background: #1c1c1c;
  box-shadow: 0 10px 40px rgba(0,0,0,0.5); overflow:hidden; padding:20px;
}
.display {
  background: #000; color: #0f0; font-size:2em; text-align:right;
  padding:15px; border-radius:10px; margin-bottom:15px;
  height:60px; overflow-x:auto; white-space:nowrap;
}
.keys {
  display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;
}
button {
  font-size:1.3em; padding:15px; border:none; border-radius:12px;
  cursor:pointer; transition: all 0.2s; background:#2c2c2c; color:white;
}
button:active { transform:scale(0.95); background:#555; }
.op { background:#ff9500; }
.eq { background:#34c759; }
.clr { background:#ff3b30; }
</style>
</head>
<body>
<div class="calculator">
  <div id="display" class="display">0</div>
  <div class="keys">
    <button class="clr">C</button>
    <button class="bs">⌫</button>
    <button>(</button>
    <button class="op">/</button>
    <button>7</button><button>8</button><button>9</button><button class="op">*</button>
    <button>4</button><button>5</button><button>6</button><button class="op">-</button>
    <button>1</button><button>2</button><button>3</button><button class="op">+</button>
    <button>0</button><button>.</button><button class="eq">=</button>
  </div>
</div>
<script>
const display = document.getElementById("display");
let expression = "";

// Update display
const updateDisplay = () => display.textContent = expression || "0";

// Handle button input
document.querySelectorAll("button").forEach(btn => {
  btn.addEventListener("click", () => handleInput(btn.textContent));
});

// Keyboard support
document.addEventListener("keydown", e => {
  const key = e.key;
  if(/[0-9+\-*/().]/.test(key)) handleInput(key);
  else if(key === "Enter") calculate();
  else if(key === "Backspace") backspace();
  else if(key === "Escape") clearDisplay();
});

// Handle input
function handleInput(val){
  if(val === "C") clearDisplay();
  else if(val === "=") calculate();
  else if(val === "⌫") backspace();
  else expression += val;
  updateDisplay();
}

// Clear display
function clearDisplay(){
  expression = "";
  updateDisplay();
}

// Backspace
function backspace(){
  expression = expression.slice(0, -1);
  updateDisplay();
}

// Calculate function
function calculate(){
  try {
    // Evaluate using JS's eval safely
    const result = Function('"use strict"; return (' + expression + ')')();
    expression = result.toString();
    updateDisplay();
  } catch(err){
    expression="Error";
    updateDisplay();
  }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
