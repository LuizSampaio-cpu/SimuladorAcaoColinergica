# Simulador de Atividade Cardíaca

Este projeto implementa um simulador interativo de atividade cardíaca com base em diferentes drogas aplicadas a um paciente. Ele combina visualizações dinâmicas, gráficos de pressão arterial e animações de batimentos cardíacos para ilustrar os efeitos fisiológicos das substâncias administradas.

## Funcionalidades

- **Animação de Batimentos Cardíacos**: Representação visual alternando entre sístole e diástole.
- **Simulação de Efeitos de Drogas**: Gráficos interativos que mostram o impacto de diversas drogas na pressão arterial ao longo do tempo.
- **Interface Intuitiva**: Interface gráfica desenvolvida com PyQt5 para facilitar a interação.
- **Personalização de Efeitos**: Ajuste de velocidades de animação e gráficos para cada substância.
- **Exportação de Gráficos**: Salve os gráficos gerados em formato PDF.

## Drogas Suportadas

O simulador suporta os seguintes fármacos (doses simuladas para um paciente de 10 kg):
- Noradrenalina (20 mcg)
- Adrenalina (20 mcg)
- Isoprenalina (20 mcg)
- Efedrina (5 mg)
- Acetilcolina (20 mcg)
- Pilocarpina (1,5 mg)
- Alfabloqueador
- Neostigmina (0,5 mg)
- Nicotina (300 mg)
- Propanolol (10 mg)
- Atropina (10 mg)
- Hexametonio (20 mg)

Cada droga afeta a pressão arterial e a frequência cardíaca de forma distinta, ilustrada no gráfico e na animação.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **PyQt5**: Framework para desenvolvimento da interface gráfica.
- **Matplotlib**: Biblioteca para visualização de dados e gráficos.
- **Numpy**: Processamento de dados numéricos.

## Como Executar

### Pré-requisitos
Certifique-se de ter Python 3.7 ou superior instalado. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

### Execução
Clone este repositório e execute o simulador:
```bash
git clone https://github.com/seu-usuario/simulador-cardíaco.git
cd simulador-cardíaco
python main.py
```

### Arquivo `requirements.txt`
Inclua o seguinte conteúdo no arquivo `requirements.txt`:
```
PyQt5>=5.15.7
matplotlib>=3.4.3
numpy>=1.21.0
```

## Estrutura do Projeto

```plaintext
simulador-cardíaco/
├── main.py              # Código principal
├── assets/              # Imagens usadas na interface
│   ├── Sístole.jpg
│   └── Diástole.jpg
├── README.md            # Este arquivo
├── requirements.txt     # Dependências do projeto
└── LICENSE              # Licença do projeto
```

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE). Sinta-se à vontade para usá-lo e modificá-lo.

## Contribuições

Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do repositório.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça um commit das suas alterações:
   ```bash
   git commit -m "Adiciona nova funcionalidade"
   ```
4. Envie suas alterações:
   ```bash
   git push origin minha-feature
   ```
5. Abra um pull request.

## Contato

Criado por [Luiz Sampaio Horta](mailto: <luizhorta2910@gmail.com>), aluno do curso de Bacharelado de Sistemas de Informação do Campus Serra do IFES, sob a orientação do professor Dr. Sérgio Nery Simões. Para dúvidas ou sugestões, entre em contato.

---

**Nota:** Este simulador foi desenvolvido com fins educacionais e pode não refletir a precisão de aplicações médicas reais.
