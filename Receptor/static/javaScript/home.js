let envio = {
  modo: null,
  enquadramento: null,
  deteccao: null,
  text: null,
  erro: null,
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
    { src: "static/imagens/analogico//Sinal FSK.png", alt: "Sinal FSK" },
    { src: "static/imagens/analogico//Sinal PSK.png", alt: "Sinal PSK" },
    { src: "static/imagens/digital/Sinal Bipolar.png", alt: "Sinal Bipolar" },
    {
      src: "static/imagens/digital/Sinal Manchester.png",
      alt: "Sinal Manchester",
    },
    { src: "static/imagens/digital/Sinal NRZ.png", alt: "Sinal NRZ" },
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

// Função para exibir a imagem em tela cheia
function expandirImagem(element) {
  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modalImg");

  modal.style.display = "flex"; // Torna o modal visível
  modalImg.src = element.src; // Define a imagem do modal para a que foi clicada
  modalImg.alt = element.alt; // Define a descrição da imagem
}

// Função para fechar o modal
function fecharModal() {
  document.getElementById("modal").style.display = "none";
}

// Função para capturar a porcentagem de erro digitada pelo usuário
document.getElementById("erro").addEventListener("input", function () {
  envio.erro = this.value;
  console.log("Porcentagem de erro:", envio.erro);
});

// function enviarConfiguracoes() {
//   // Verifica se todos os campos estão preenchidos
//   if (
//     !envio.modo ||
//     !envio.enquadramento ||
//     !envio.deteccao ||
//     !envio.text ||
//     envio.erro === null
//   ) {
//     alert("Erro: Todos os campos devem ser preenchidos antes do envio!");
//     return;
//   }

//   // Valida se o erro está entre 0 e 100
//   if (envio.erro < 0 || envio.erro > 100) {
//     alert("Erro: A porcentagem de erro deve estar entre 0 e 100!");
//     return;
//   }

//   console.log("Enviando dados:", envio);

//   // Envia os dados para o backend
//   fetch("/processar_dados", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(envio),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       if (data.erro) {
//         console.error("Erro do servidor:", data.erro);
//         document.getElementById("resultado").value = "Erro: " + data.erro;
//       } else {
//         console.log("Resposta do servidor:", data.resultado);
//         document.getElementById("resultado").value = data.resultado;
//       }
//     })
//     .catch((error) => {
//       console.error("Erro na requisição:", error);
//       document.getElementById("resultado").value =
//         "Erro ao conectar com o servidor.";
//     });
// }

function enviarConfiguracoes() {
  if (
    !envio.modo ||
    !envio.enquadramento ||
    !envio.deteccao ||
    !envio.text ||
    envio.erro === null
  ) {
    alert("Erro: Todos os campos devem ser preenchidos antes do envio!");
    return;
  }

  if (envio.erro < 0 || envio.erro > 100) {
    alert("Erro: A porcentagem de erro deve estar entre 0 e 100!");
    return;
  }

  console.log("Enviando dados para o Flask...", envio);

  fetch("http://127.0.0.1:5000/processar_dados", {
    method: "POST", // 🔹 IMPORTANTE: O método precisa ser POST
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(envio), // 🔹 Envia os dados corretamente
  })
    .then((response) => {
      console.log("Resposta do servidor recebida:", response);
      if (!response.ok) {
        throw new Error(`Erro no servidor: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.erro) {
        console.error("Erro do servidor:", data.erro);
        document.getElementById("resultado").value = "Erro: " + data.erro;
      } else {
        console.log("Resposta do servidor:", data.resultado);
        document.getElementById("resultado").value = data.resultado;
      }
    })
    .catch((error) => {
      console.error("Erro na requisição:", error);
      document.getElementById("resultado").value =
        "Erro ao conectar com o servidor.";
    });
}
