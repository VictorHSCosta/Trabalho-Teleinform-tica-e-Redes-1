let selected;

//variaveis e constantes

const images = [
  { src: "../static/images/analogico/Sinal ASK.png", alt: "Sinal ASK", tipo: "analogico" },
  { src: "../static/images/analogico/Sinal FSK.png", alt: "Sinal FSK", tipo: "analogico" },
  { src: "../static/images/analogico/Sinal PSK.png", alt: "Sinal PSK", tipo: "analogico" },
  { src: "../static/images/digital/Sinal Bipolar.png", alt: "Sinal Bipolar", tipo: "digital" },
  { src: "../static/images/digital/Sinal Manchester.png", alt: "Sinal Manchester", tipo: "digital" },
  { src: "../static/images/digital/Sinal NRZ.png", alt: "Sinal NRZ", tipo: "digital" },
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

  // Impede a seleção de imagens analógicas
  if (img.classList.contains("analogico")) {
    alert("Não é possível selecionar sinais analógicos.");
    return;
  }

  const updateElement = selected;
  selected = element;

  try {
    updateElement.style.border = "none";
  } catch (error) {
    console.log("Nenhum elemento selecionado ainda.");
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

  // Limpa o container para evitar duplicações
  container2.innerHTML = "";

  // Cria seções para analógicos e digitais
  const tituloAnalogico = document.createElement("h3");
  tituloAnalogico.innerText = "Sinais Analógicos (Exibição Apenas)";
  container2.appendChild(tituloAnalogico);

  const containerAnalogico = document.createElement("div");
  containerAnalogico.id = "analogico";
  containerAnalogico.style.display = "flex";
  containerAnalogico.style.flexWrap = "wrap";
  container2.appendChild(containerAnalogico);

  const tituloDigital = document.createElement("h3");
  tituloDigital.innerText = "Sinais Digitais (Selecionáveis)";
  container2.appendChild(tituloDigital);

  const containerDigital = document.createElement("div");
  containerDigital.id = "digital";
  containerDigital.style.display = "flex";
  containerDigital.style.flexWrap = "wrap";
  container2.appendChild(containerDigital);

  // Adiciona imagens nos containers apropriados
  images.forEach((imgData, index) => {
    const button = document.createElement("button");
    const img = document.createElement("img");
    img.src = `${imgData.src}?t=${new Date().getTime()}`;
    img.alt = imgData.alt;

    if (imgData.tipo === "analogico") {
      img.classList.add("analogico");
      containerAnalogico.appendChild(button);
    } else {
      img.classList.add("digital");
      button.onclick = () => select(button); // Apenas sinais digitais podem ser selecionados
      containerDigital.appendChild(button);
    }

    button.appendChild(img);
  });
  
  const container4 = document.getElementById("container4");
  container4.style.display = "flex";
}



async function abrirConfiguracoes() {}

async function enviarImagem() {
  if (!selected) {
      alert("Selecione uma imagem para enviar");
      return;
  }

  const img = selected.children[0];
  const tipo = img.alt.split(" ")[1]; // Extrai o tipo de modulação do 'alt'

  console.log("Tipo de modulação selecionado:", tipo); // Log para verificar o valor

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
  const bitsOriginais = document.getElementById("resultado").innerHTML.trim(); // Limpa espaços
  const erro = document.getElementById("erro").value.trim(); // Limpa espaços

  // Validação de entrada
  if (!bitsOriginais) {
      alert("O trem de bits original está vazio. Converta um texto antes de aplicar o erro.");
      return;
  }
  if (erro === "" || isNaN(erro) || erro < 0 || erro > 100) {
      alert("Digite um valor de erro válido entre 0 e 100.");
      return;
  }

  try {
      // Envia o trem de bits e o erro para o backend
      const response = await fetch("/calcular_erro", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ bits: bitsOriginais, erro }),
      });

      if (response.ok) {
          const data = await response.json();
          const bitsComErro = data.bits_com_erro; // Fluxo de bits com erro
          const posicoesErro = data.posicoes_erro; // Posições dos bits alterados

          // Gera HTML para destacar os bits alterados
          const bitsFormatados = bitsComErro
              .split("")
              .map((bit, index) =>
                  posicoesErro.includes(index) ? `<span style="color: red;">${bit}</span>` : bit
              )
              .join("");

          // Atualiza a caixa de texto com o resultado
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

