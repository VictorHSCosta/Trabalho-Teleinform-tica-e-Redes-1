let selected;

// Variables and constants
const images = [
  {
    src: "../static/images/analogico/Sinal ASK.png",
    alt: "Sinal ASK",
    tipo: "analogico",
  },
  {
    src: "../static/images/analogico/Sinal FSK.png",
    alt: "Sinal FSK",
    tipo: "analogico",
  },
  {
    src: "../static/images/analogico/Sinal PSK.png",
    alt: "Sinal PSK",
    tipo: "analogico",
  },
  {
    src: "../static/images/digital/Sinal Bipolar.png",
    alt: "Sinal Bipolar",
    tipo: "digital",
  },
  {
    src: "../static/images/digital/Sinal Manchester.png",
    alt: "Sinal Manchester",
    tipo: "digital",
  },
  {
    src: "../static/images/digital/Sinal NRZ.png",
    alt: "Sinal NRZ",
    tipo: "digital",
  },
];

// Functions
async function MenuErro(abrir) {
  const container3 = document.getElementById("container3");
  container3.classList.toggle("hidden", !abrir);
  if (abrir) {
    container3.classList.add("flex", "flex-col");
  }
}

function select(element) {
  const img = element.querySelector("img");

  if (img.classList.contains("analogico")) {
    alert("Não é possível selecionar sinais analógicos.");
    return;
  }

  if (selected) {
    selected.classList.remove("border-2", "border-black");
  }

  selected = element;
  element.classList.add("border-2", "border-black");

  const sinal = document.getElementById("sinal-a-enviar");
  sinal.innerText = `Enviar ${img.alt}`;
}

async function atualizatexto() {
  const text = document.getElementById("entrada").value;

  if (!text) {
    document.getElementById("resultado").value = "";
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
      document.getElementById("resultado").value = data.bits_array;
    }

    await atualizaImagem();
    MenuErro(true);
  } catch (error) {
    console.log(error);
  }
}

async function atualizaImagem() {
  const container2 = document.getElementById("container2");
  container2.classList.remove("hidden");
  container2.classList.add("flex", "flex-col");

  container2.innerHTML = "";

  const createSection = (title, id) => {
    const section = document.createElement("div");
    section.className = "mb-8";

    const h3 = document.createElement("h3");
    h3.className = "text-xl font-semibold mb-4";
    h3.innerText = title;
    section.appendChild(h3);

    const container = document.createElement("div");
    container.id = id;
    container.className =
      "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4";
    section.appendChild(container);

    return section;
  };

  container2.appendChild(
    createSection("Sinais Analógicos (Exibição Apenas)", "analogico")
  );
  container2.appendChild(
    createSection("Sinais Digitais (Selecionáveis)", "digital")
  );

  images.forEach((imgData) => {
    const button = document.createElement("button");
    button.className =
      "bg-transparent border-none transition-transform duration-300 ease-in-out cursor-pointer hover:scale-105 shadow-md rounded-lg overflow-hidden";

    const img = document.createElement("img");
    img.src = `${imgData.src}?t=${new Date().getTime()}`;
    img.alt = imgData.alt;
    img.className = "w-full h-auto";

    if (imgData.tipo === "analogico") {
      img.classList.add("analogico", "opacity-60", "cursor-not-allowed");
      document.getElementById("analogico").appendChild(button);
    } else {
      img.classList.add("digital");
      button.onclick = () => select(button);
      document.getElementById("digital").appendChild(button);
    }

    button.appendChild(img);
  });

  const container4 = document.getElementById("container4");
  container4.classList.remove("hidden");
  container4.classList.add("flex", "flex-col");
}

async function enviarImagem() {
  if (!selected) {
    alert("Selecione uma imagem para enviar");
    return;
  }

  const img = selected.querySelector("img");
  const tipo = img.alt.split(" ")[1];

  console.log("Tipo de modulação selecionado:", tipo);

  const bits = document.getElementById("resultado").value;

  if (!bits) {
    alert("Digite algo para converter");
    return;
  }

  const erro = document.getElementById("erro").value;

  if (erro === "" || erro < 0 || erro > 100) {
    alert("Digite um valor de erro entre 0 e 100");
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

async function adicionarErro() {
  const bitsOriginais = document.getElementById("resultado").value.trim();
  const erro = document.getElementById("erro").value.trim();

  if (!bitsOriginais) {
    alert(
      "O trem de bits original está vazio. Converta um texto antes de aplicar o erro."
    );
    return;
  }
  if (erro === "" || isNaN(erro) || erro < 0 || erro > 100) {
    alert("Digite um valor de erro válido entre 0 e 100.");
    return;
  }

  try {
    const response = await fetch("/calcular_erro", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ bits: bitsOriginais, erro }),
    });

    if (response.ok) {
      const data = await response.json();
      const bitsComErro = data.bits_com_erro;
      const posicoesErro = data.posicoes_erro;

      const bitsFormatados = bitsComErro
        .split("")
        .map((bit, index) =>
          posicoesErro.includes(index)
            ? `<span class="text-red-500">${bit}</span>`
            : bit
        )
        .join("");

      const resultadoComErro = document.getElementById("resultado-com-erro");
      resultadoComErro.innerHTML = bitsFormatados;
    } else {
      const errorData = await response.json();
      alert(`Erro: ${errorData.erro}`);
    }
  } catch (error) {
    console.log("Erro ao calcular o erro:", error);
    alert("Ocorreu um erro ao calcular o erro.");
  }
}

// Event listeners
document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("acrescentar-erro")
    .addEventListener("click", adicionarErro);
});
