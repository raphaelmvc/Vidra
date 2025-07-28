document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('downloadForm');
  const mensagem = document.getElementById('mensagem');

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    // Limpar mensagem anterior
    mensagem.innerHTML = '⏳ Processando download...';

    const dados = {
      url: form.url.value.trim(),
      plataforma: form.plataforma.value,
      tipo: form.tipo.value,
      nome: form.nome.value.trim() || null,
    };

    try {
      const resposta = await fetch('/baixar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dados),
      });

      const resultado = await resposta.json();

      if (resposta.ok) {
        mensagem.innerHTML = `✅ ${resultado.mensagem}`;
        mensagem.style.color = '#00cc88';
      } else {
        mensagem.innerHTML = `❌ Erro: ${
          resultado.detail || 'Falha no download.'
        }`;
        mensagem.style.color = '#ff5555';
      }
    } catch (erro) {
      console.error(erro);
      mensagem.innerHTML =
        '❌ Erro inesperado. Verifique sua conexão ou tente novamente.';
      mensagem.style.color = '#ff5555';
    }
  });
});
