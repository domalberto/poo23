let gastos = [];
let total = 0;

const categoriaSelec = document.getElementById('select-categoria');
const quantImput = document.getElementById('imput-quant');
const dataInput = document.getElementById('imput-data');
const addBtn = document.getElementById('add-btn');
const gastosBody = document.getElementById('lista-gastos-body');
const totalCell = document.getElementById('gasto-total');

addBtn.addEventListener('click', function() {
    const categoria = categoriaSelec.value;
    const quant = Number(quantImput.value);
    const data = dataInput.value;

    if (categoria === '') {
        alert('Por favor selecione uma categoria');
        return;
    }
    if (isNaN(quant) || quant <=0 ) {
        alert('Por favor coloque uma quantidade valida')
        return;
    }
    if(data === '') {
        alert('por favor selecione uma data')
        return;
    }
    gastos.push({categoria, quant, data});

    total += quant;
    totalCell.textContent = total;

    const novaLinha = gastosBody.insertRow();

    const categoriaCell = novaLinha.insertCell();
    const quantCell = novaLinha.insertCell();
    const dataCell = novaLinha.insertCell();
    const deleteCell = novaLinha.insertCell();
    const deleteBtn = document.createElement('button');

    deleteBtn.textContent = 'Deletar';
    deleteBtn.classList.add('delete-btn');
    deleteBtn.addEventListener('click', function() {
        gastos.splice(gastos.indexOf(gastos), 1);

        total -= gastos.quant;
        totalCell.textContent = total;

        gastosBody.removeChild(novaLinha);
    });

    const gasto = gastos[gastos.length - 1];
    categoriaCell.textContent = gasto.categoria;
    quantCell.textContent = gasto.quant;
    dataCell.textContent = gasto.data;
    deleteCell.appendChild(deleteBtn);

});
