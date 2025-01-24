let selected;

//variaveis e constantes

const images = [
  { src: "../static/images/analogico/Sinal ASK.png", alt: "Sinal ASK" },
  { src: "../static/images/analogico/Sinal FSK.png", alt: "Sinal FSK" },
  { src: "../static/images/analogico/Sinal PSK.png", alt: "Sinal PSK" },
  { src: "../static/images/digital/Sinal Bipolar.png", alt: "Sinal Bipolar" },
  {
    src: "../static/images/digital/Sinal Manchester.png",
    alt: "Sinal Manchester",
  },
  { src: "../static/images/digital/Sinal NRZ.png", alt: "Sinal NRZ" },
];

//funcoes js

async function MenuErro(abrir) {
  const container3 = document.getElementById("container3");
  if (abrir) {
    container3.style.display = "flex";
    container3.style.flexDirection = "column";
    return;
  }
  container3.style.display = "none";
}

function select(element) {
  const img = element.children[0];
  const updateElement = selected;
  selected = element;

  try {
    updateElement.style.border = "none";
  } catch (error) {
    console.log("No element selected yet");
  }

  element.style.border = "solid 2px #000";
  const sinal = document.getElementById("sinal-a-enviar");
  sinal.innerText = `Enviar ${img.alt}`;
}

async function atualizatexto() {
  const text = document.getElementById("entrada").value;

  if (!text) {
    document.getElementById("resultado").innerHTML = "";
    alert("Digite algo para converter");
    const containerImagens = document.getElementById("container2");
    containerImagens.innerHTML = "";
    MenuErro(false);
    return;
  }

  try {
    const response = await fetch(`/get_bits?text=${encodeURIComponent(text)}`);

    if (response.ok) {
      const data = await response.json();

      document.getElementById("resultado").innerHTML = data.bits_array;
    }

    await atualizaImagem();
    MenuErro(true);
  } catch (error) {
    console.log(error);
  }
}

async function atualizaImagem() {
  const container2 = document.getElementById("container2");
  container2.style.display = "flex";
  const Imagens = document.querySelectorAll("#imagens >  button > img");

  console.log(images);

  Imagens.forEach((image, index) => {
    image.innerHTML = "";
    image.src = `${images[index].src}?t=${new Date().getTime()}`;
    image.alt = images[index].alt;
  });

  const containerImagens = document.getElementById("container2");
  const div = document.createElement("div");
  containerImagens.appendChild(div);
  const container4 = document.getElementById("container4");
  container4.style.display = "flex";
}

async function abrirConfiguracoes() {}

async function enviarImagem() {
  if (!selected) {
    alert("Selecione uma imagem para enviar");
    return;
  }

  const bits = document.getElementById("resultado").value;

  if (!bits) {
    alert("Digite algo para converter");
    return;
  }

  const erro = document.getElementById("erro").value;

  if (erro === "") {
    alert("Digite um valor de erro");
    return;
  }

  if (erro < 0 || erro > 100) {
    alert("Digite um valor de erro entre 0 e 100");
    return;
  }

  const tipo = document.getElementById("sinal-a-enviar").innerText;

  console.log(tipo);

  if (tipo === "") {
    alert("Selecione um tipo de sinal para enviar");
    return;
  }

  try {
    const response = await fetch("/enviar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ bits, erro, tipo }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data);
    } else {
      const errorData = await response.json();
      console.log("Erro na resposta:", errorData);
    }
  } catch (error) {
    console.log("Erro na requisição:", error);
  }
}
