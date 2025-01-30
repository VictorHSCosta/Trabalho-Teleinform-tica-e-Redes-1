let envio = {
  modo: null,
  enquadramento: null,
  deteccao: null,
  text: null,
};

// Função para enviar texto para o Flask e obter bits codificados
function converterTextoParaBits() {
  const inputText = document.getElementById("entrada").value;

  if (!inputText.trim()) {
    console.error("Erro: O campo de entrada está vazio.");
    document.getElementById("resultado").value = "Digite um texto.";
    return;
  }

  // Atualiza o objeto envio
  envio.text = inputText;

  // Faz uma requisição para o Flask
  fetch(`/get_bits?text=${encodeURIComponent(inputText)}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erro ao obter bits do servidor.");
      }
      return response.json();
    })
    .then((data) => {
      document.getElementById("resultado").value = data.bits_array;
      recarregarImagens(); // Atualiza as imagens após obter os bits
    })
    .catch((error) => {
      console.error("Erro ao buscar bits:", error);
      document.getElementById("resultado").value = "Erro ao processar.";
    });
}

// Função para recarregar as imagens
function recarregarImagens() {
  console.log("Recarregando imagens...");

  const images = [
    { src: "static/imagens/analogico/Sinal ASK.png", alt: "Sinal ASK" },
    { src: "../imagens/analogico/Sinal FSK.png", alt: "Sinal FSK" },
    { src: "../imagens/analogico/Sinal PSK.png", alt: "Sinal PSK" },
    { src: "../imagens/digital/Sinal Bipolar.png", alt: "Sinal Bipolar" },
    { src: "../imagens/digital/Sinal Manchester.png", alt: "Sinal Manchester" },
    { src: "../imagens/digital/Sinal NRZ.png", alt: "Sinal NRZ" },
  ];

  // Atualizar imagens analógicas
  const imagensAnalogicas = document.querySelectorAll("#imagens_analogico img");
  imagensAnalogicas.forEach((img, index) => {
    img.src = `${images[index].src}?t=${new Date().getTime()}`;
    img.alt = images[index].alt;
  });

  // Atualizar imagens digitais
  const imagensDigitais = document.querySelectorAll("#imagens_digital img");
  imagensDigitais.forEach((img, index) => {
    img.src = `${images[index + 3].src}?t=${new Date().getTime()}`;
    img.alt = images[index + 3].alt;
  });
}

function selecionarModo(element) {
  // Verifica se já existe um botão selecionado e redefine sua cor para cinza
  if (envio.modo !== null) {
    let btnAnterior = document.querySelector(`[data-modo="${envio.modo}"]`);
    if (btnAnterior) {
      btnAnterior.classList.remove("bg-green-600");
      btnAnterior.classList.add("bg-gray-600");
    }
  }

  // Atualiza o valor armazenado
  envio.modo = element.getAttribute("data-modo");

  // Atualiza a cor do botão selecionado
  element.classList.remove("bg-gray-600");
  element.classList.add("bg-green-600");

  console.log("Modo selecionado:", envio.modo);
}

function selecionarEnquadramento(element) {
  // Verifica se já existe um botão selecionado e redefine sua cor para cinza
  if (envio.enquadramento !== null) {
    let btnAnterior = document.querySelector(
      `[data-enquadramento="${envio.enquadramento}"]`
    );
    if (btnAnterior) {
      btnAnterior.classList.remove("bg-yellow-600");
      btnAnterior.classList.add("bg-gray-600");
    }
  }

  // Atualiza o valor armazenado
  envio.enquadramento = element.getAttribute("data-enquadramento");

  // Atualiza a cor do botão selecionado
  element.classList.remove("bg-gray-600");
  element.classList.add("bg-yellow-600");

  console.log("Enquadramento selecionado:", envio.enquadramento);
}

function selecionarDeteccao(element) {
  // Verifica se já existe um botão selecionado e redefine sua cor para cinza
  if (envio.deteccao !== null) {
    let btnAnterior = document.querySelector(
      `[data-deteccao="${envio.deteccao}"]`
    );
    if (btnAnterior) {
      btnAnterior.classList.remove("bg-purple-600");
      btnAnterior.classList.add("bg-gray-600");
    }
  }

  // Atualiza o valor armazenado
  envio.deteccao = element.getAttribute("data-deteccao");

  // Atualiza a cor do botão selecionado
  element.classList.remove("bg-gray-600");
  element.classList.add("bg-purple-600");

  console.log("Detecção selecionada:", envio.deteccao);
}

function enviarConfiguracoes() {
  console.log("Modo:", envio.modo);
  console.log("Enquadramento:", envio.enquadramento);
  console.log("Detecção:", envio.deteccao);

  if (!envio.modo || !envio.enquadramento || !envio.deteccao) {
    console.error(
      "Erro: Todos os campos devem ser selecionados antes do envio!"
    );
    return;
  }

  // Aqui você pode enviar as configurações para o backend via fetch
}
