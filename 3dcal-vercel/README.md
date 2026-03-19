# 3dcal - Calculadora de Impressões 3D

Versão web da calculadora 3dcal para deploy no Vercel.

## Funcionalidades

- 🌙 **Tema Escuro/Claro**: Interface adaptável com persistência de preferência
- 🖥️ **Design Responsivo**: Funciona em desktop e mobile
- ⚡ **Cálculos em Tempo Real**: API REST para processamento rápido
- 📊 **Análise Detalhada**: Breakdown completo de custos
- 💾 **Copiar Resultados**: Um clique para copiar o preço final
- ⌨️ **Atalhos**: Enter para calcular, navegação por teclado

## Tecnologias

- **Backend**: Flask (Python)
- **Frontend**: HTML5 + Tailwind CSS + JavaScript
- **Deploy**: Vercel Serverless Functions
- **Icons**: Lucide Icons

## Estrutura do Projeto

```
3dcal-web/
├── app.py              # Backend Flask
├── templates/
│   └── index.html      # Frontend
├── requirements.txt     # Dependências Python
├── vercel.json        # Config Vercel
├── .gitignore         # Arquivos ignorados
└── README.md          # Este arquivo
```

## Deploy no Vercel

1. **Instalar Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Fazer login**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd 3dcal-web
   vercel --prod
   ```

4. **Configurar domínio**:
   ```bash
   vercel domains add calcular3d.com
   ```

## Desenvolvimento Local

1. **Criar ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

2. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar localmente**:
   ```bash
   python app.py
   ```

4. Acessar `http://localhost:5000`

## API Endpoints

### POST /api/calculate

Calcula custos e preço final.

**Request Body**:
```json
{
  "printer": "A1",
  "weight": 100.0,
  "filament_price": 200.0,
  "time": 2.5,
  "profit": 25.0,
  "quantity": 1
}
```

**Response**:
```json
{
  "costs": {
    "material": 20.00,
    "energy": 0.27,
    "wear": 5.00,
    "failure": 2.53,
    "maintenance": 2.53,
    "depreciation": 0.57,
    "roi": 1.04,
    "total_per_piece": 31.94
  },
  "results": {
    "total_cost": 31.94,
    "sale_price": 39.93,
    "price_per_piece": 39.93,
    "profit_amount": 7.99,
    "profit_percentage": 25.0
  },
  "quantity": 1
}
```

## Cálculos Implementados

- **Material**: Peso × Preço do filamento
- **Energia**: Consumo × Tempo × Custo/kWh  
- **Desgaste**: Tempo × Custo/hora
- **Falhas**: Custo base × Taxa de falhas
- **Manutenção**: Custo base × Taxa de manutenção
- **Depreciação**: Valor máquina ÷ (Vida útil × horas)
- **ROI**: Valor máquina ÷ (Meses para pagar × dias × horas)

## Licença

Desenvolvido por João Pedro de Brito Amaro
