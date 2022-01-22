var greeting = "hola, ";
const para = document.createElement("div");
para.className = "overlay"

const text = document.createElement("p");
text.innerText="bob";

para.appendChild(text);

const element = document.getElementsByTagName("body")[0];
element.appendChild(para);
