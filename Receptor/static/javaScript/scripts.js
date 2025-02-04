document.addEventListener("DOMContentLoaded", () => {
  function buscarDados() {
    fetch("http://localhost:3000/dados") // Tente com 'localhost' primeiro
      .then((response) => response.json())
      .then((dados) => {
        console.log("Dados recebidos:", dados);

        // Atualiza os elementos da página
        document.getElementById("finalText").value = dados.texto;
        document.getElementById("receivedBits").value = dados.bits;
        document.getElementById("error").innerText = dados.correcao;
        document.getElementById("metodo").innerText = dados.enquadramento;
        document.getElementById("receivedModulacao").innerText =
          dados.modulacao;

        // Atualiza a imagem
        atualizarImagem(dados.modulacao);
      })
      .catch((error) => console.error("Erro ao buscar os dados:", error));
  }

  // Chama a função imediatamente e depois a cada 1 segundo
  buscarDados();
  setInterval(buscarDados, 1000);
});

function atualizarImagem(qual) {
  const imagem = document.getElementById("imagemtexto");
  const imagens = {
    NRZ: {
      src: "static/imagens/digital/Sinal NRZ.png",
      alt: "Sinal NRZ",
    },
    Manchester: {
      src: "static/imagens/digital/Sinal Manchester.png",
      alt: "Sinal Manchester",
    },
    Bipolar: {
      src: "static/imagens/digital/Sinal Bipolar.png",
      alt: "Sinal Bipolar",
    },
  };

  // Se a entrada não estiver no objeto, usa NRZ como padrão
  const imagemSelecionada = imagens[qual] || imagens["NRZ"];

  // Atualiza a imagem
  imagem.src = `${imagemSelecionada.src}?t=${new Date().getTime()}`;
  imagem.alt = imagemSelecionada.alt;

  console.log(`Imagem atualizada para: ${imagemSelecionada.alt}`);
}

// Função para exibir a imagem em tela cheia
function expandirImagem() {
  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modalImg");
  const imagem = document.getElementById("imagemtexto");

  modal.style.display = "flex"; // Torna o modal visível
  modalImg.src = imagem.src; // Define a imagem do modal para a que foi clicada
  modalImg.alt = imagem.alt; // Define a descrição da imagem
}

// Função para fechar o modal
function fecharModal() {
  document.getElementById("modal").style.display = "none";
}
