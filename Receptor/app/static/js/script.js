let select;

function selectElement(element) {
  legacy = select;
  select = element;

  try {
    legacy.style.backgroundColor = "transparent";
    legacy.style.color = "#000";
  } catch (error) {
    console.log("No element selected yet");
  }

  element.style.backgroundColor = "#00ca9e";
  element.style.color = "#fff";
}

async function atualizarBits() {
  try {
    const response = await fetch("/receber");

    if (response.ok) {
      const data = await response.json();
      document.getElementById("bits-com-erro").innerHTML = data.bits_com_erro;
      document.getElementById("bits-corrigidos").innerText = data.bits_corrigidos;
    } else {
      console.error("Erro ao receber dados:", response.statusText);
    }
  } catch (error) {
    console.error("Erro na requisição:", error);
  }
}

// Chama a função para atualizar os bits ao carregar a página
document.addEventListener("DOMContentLoaded", atualizarBits);

async function receberDados() {
  try {
    const response = await fetch('/receber', {
      method: 'GET',
    });

    if (response.ok) {
      const data = await response.json();
      document.getElementById('fluxo-destacado').innerHTML = data.fluxo_destacado;
      document.getElementById('fluxo-corrigido').innerText = data.fluxo_corrigido;
    } else {
      console.error('Erro ao receber os dados do servidor.');
    }
  } catch (error) {
    console.error('Erro na requisição:', error);
  }
}
