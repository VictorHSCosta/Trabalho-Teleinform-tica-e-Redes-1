document.addEventListener("DOMContentLoaded", () => {
  // Conecta ao servidor Socket.IO
  const socket = io();

  // Escuta o evento 'atualizacao' emitido pelo servidor
  socket.on("atualizacao", (dados) => {
    console.log("Dados recebidos:", dados);

    // Atualiza os elementos da página com os dados recebidos
    document.getElementById("finalText").value = dados.texto;
    document.getElementById("receivedBits").value = dados.bits;
    document.getElementById("error").innerText = dados.correcao;
    document.getElementById("metodo").innerText = dados.enquadramento;
    // Caso queira exibir também o tipo de modulação:
    // document.getElementById('algumElemento').innerText = dados.modulacao;
  });
});
