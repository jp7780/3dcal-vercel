from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações da calculadora
CONFIG = {
    "printers": {
        "A1": {"name": "A1", "power_kw": 0.12},
        "P2S": {"name": "P2S", "power_kw": 0.15}
    },
    "costs": {
        "energy_per_kwh": 0.90,
        "wear_per_hour": 2.00,
        "failure_rate": 10.0,
        "maintenance_rate": 10.0
    },
    "investment": {
        "machine_value": 10000.0,
        "useful_life_years": 5.0,
        "hours_per_day": 8.0,
        "days_per_month": 30.0,
        "months_to_pay": 24.0
    }
}

def calculate_costs(printer_key, weight_g, filament_price_per_kg, time_h, profit_pct, quantity=1):
    """Calcula custos e preço final"""
    printer = CONFIG["printers"][printer_key]
    costs = CONFIG["costs"]
    invest = CONFIG["investment"]
    
    # Custo material
    material_cost = (weight_g / 1000) * filament_price_per_kg
    
    # Custo energia
    energy_cost = printer["power_kw"] * time_h * costs["energy_per_kwh"]
    
    # Custo desgaste
    wear_cost = time_h * costs["wear_per_hour"]
    
    # Custo falhas (% adicional)
    failure_cost = (material_cost + energy_cost + wear_cost) * (costs["failure_rate"] / 100)
    
    # Custo manutenção (% adicional)
    maintenance_cost = (material_cost + energy_cost + wear_cost) * (costs["maintenance_rate"] / 100)
    
    # Depreciação por hora
    depreciation_per_hour = invest["machine_value"] / (invest["useful_life_years"] * 365 * 24)
    depreciation_cost = time_h * depreciation_per_hour
    
    # ROI por hora
    roi_per_hour = invest["machine_value"] / (invest["months_to_pay"] * invest["days_per_month"] * invest["hours_per_day"])
    roi_cost = time_h * roi_per_hour
    
    # Custo total por peça
    total_cost_per_piece = material_cost + energy_cost + wear_cost + failure_cost + maintenance_cost + depreciation_cost + roi_cost
    
    # Custo total
    total_cost = total_cost_per_piece * quantity
    
    # Preço de venda
    profit_amount = total_cost * (profit_pct / 100)
    sale_price = total_cost + profit_amount
    
    # Preço por peça
    price_per_piece = sale_price / quantity
    
    return {
        "costs": {
            "material": round(material_cost, 2),
            "energy": round(energy_cost, 2),
            "wear": round(wear_cost, 2),
            "failure": round(failure_cost, 2),
            "maintenance": round(maintenance_cost, 2),
            "depreciation": round(depreciation_cost, 2),
            "roi": round(roi_cost, 2),
            "total_per_piece": round(total_cost_per_piece, 2)
        },
        "results": {
            "total_cost": round(total_cost, 2),
            "sale_price": round(sale_price, 2),
            "price_per_piece": round(price_per_piece, 2),
            "profit_amount": round(profit_amount, 2),
            "profit_percentage": round(profit_pct, 1)
        },
        "quantity": quantity
    }

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>3dcal - Calculadora 3D</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            :root {
                --primary: #00ff9c;
                --bg-dark: #121212;
                --panel-dark: #1e1e1e;
                --text-dark: #ffffff;
                --text-dim: #cccccc;
            }
            
            body {
                background-color: var(--bg-dark);
                color: var(--text-dark);
            }
            
            .panel {
                background-color: var(--panel-dark);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
            }
            
            .btn-primary {
                background-color: var(--primary);
                color: var(--bg-dark);
                font-weight: bold;
            }
            
            .btn-primary:hover {
                background-color: #00cc7a;
            }
            
            .text-primary {
                color: var(--primary);
            }
            
            .text-dim {
                color: var(--text-dim);
            }
            
            .input {
                background-color: #333333;
                border: 1px solid #555555;
                color: white;
                padding: 12px;
                border-radius: 8px;
            }
            
            .input:focus {
                outline: none;
                border-color: var(--primary);
            }
        </style>
    </head>
    <body class="min-h-screen p-8">
        <div class="container mx-auto max-w-6xl">
            <header class="text-center mb-8">
                <h1 class="text-4xl font-bold text-primary mb-2">3dcal</h1>
                <p class="text-dim">Calculadora de Impressões 3D</p>
            </header>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Left Panel - Inputs -->
                <div class="lg:col-span-1">
                    <div class="panel">
                        <h2 class="text-xl font-bold text-primary mb-4">
                            ⚙️ Configurações
                        </h2>
                        
                        <div class="space-y-4">
                            <div>
                                <label class="block text-dim text-sm font-medium mb-2">Peso (g)</label>
                                <input type="number" id="weight" class="input w-full" placeholder="0.0" step="0.1">
                            </div>
                            
                            <div>
                                <label class="block text-dim text-sm font-medium mb-2">Filamento (R$/kg)</label>
                                <input type="number" id="filament-price" class="input w-full" placeholder="0.0" step="0.01">
                            </div>
                            
                            <div>
                                <label class="block text-dim text-sm font-medium mb-2">Tempo (h)</label>
                                <input type="number" id="time" class="input w-full" placeholder="0.0" step="0.1">
                            </div>
                            
                            <div>
                                <label class="block text-dim text-sm font-medium mb-2">Lucro (%)</label>
                                <input type="number" id="profit" class="input w-full" placeholder="0.0" step="0.1">
                            </div>
                            
                            <div>
                                <label class="block text-dim text-sm font-medium mb-2">Quantidade</label>
                                <input type="number" id="quantity" class="input w-full" placeholder="1" min="1" value="1">
                            </div>
                        </div>

                        <button onclick="calculate()" class="btn-primary w-full mt-6 text-lg py-3 rounded-lg">
                            🧮 Calcular
                        </button>
                    </div>
                </div>

                <!-- Center Panel - Results -->
                <div class="lg:col-span-1">
                    <div class="panel">
                        <h2 class="text-xl font-bold text-primary mb-4">
                            📊 Resultados
                        </h2>
                        
                        <div class="text-3xl font-bold text-primary text-center p-6 bg-gray-800 rounded-lg mb-4" id="price-display">
                            R$ 0,00
                        </div>
                        
                        <div class="space-y-3">
                            <div class="flex justify-between p-3 bg-gray-800 rounded">
                                <span class="text-dim">Custo Total</span>
                                <span class="font-bold" id="total-cost">R$ 0,00</span>
                            </div>
                            
                            <div class="flex justify-between p-3 bg-gray-800 rounded">
                                <span class="text-dim">Valor por Peça</span>
                                <span class="font-bold" id="price-per-piece">R$ 0,00</span>
                            </div>
                            
                            <div class="flex justify-between p-3 bg-gray-800 rounded">
                                <span class="text-dim">Lucro</span>
                                <span class="font-bold text-primary" id="profit-amount">R$ 0,00</span>
                            </div>
                            
                            <div class="flex justify-between p-3 bg-gray-800 rounded">
                                <span class="text-dim">Margem</span>
                                <span class="font-bold" id="profit-percentage">0%</span>
                            </div>
                        </div>

                        <button onclick="copyPrice()" class="w-full mt-4 bg-gray-700 text-white py-2 rounded hover:bg-gray-600" id="copy-btn" disabled>
                            📋 Copiar Preço
                        </button>
                    </div>
                </div>

                <!-- Right Panel - Cost Breakdown -->
                <div class="lg:col-span-1">
                    <div class="panel">
                        <h2 class="text-xl font-bold text-primary mb-4">
                            📈 Detalhes do Custo
                        </h2>
                        
                        <div class="space-y-3" id="cost-breakdown">
                            <div class="flex justify-between">
                                <span class="text-dim">Material</span>
                                <span id="cost-material">R$ 0,00</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-dim">Energia</span>
                                <span id="cost-energy">R$ 0,00</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-dim">Desgaste</span>
                                <span id="cost-wear">R$ 0,00</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-dim">Falhas</span>
                                <span id="cost-failure">R$ 0,00</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-dim">Manutenção</span>
                                <span id="cost-maintenance">R$ 0,00</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-dim">Depreciação</span>
                                <span id="cost-depreciation">R$ 0,00</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-dim">ROI</span>
                                <span id="cost-roi">R$ 0,00</span>
                            </div>
                            <div class="border-t pt-3 mt-3">
                                <div class="flex justify-between font-bold">
                                    <span>Total por Peça</span>
                                    <span id="cost-total-per-piece">R$ 0,00</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let lastResult = null;

            // Format currency
            function formatCurrency(value) {
                return new Intl.NumberFormat('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                }).format(value);
            }

            // Calculate function
            async function calculate() {
                const weight = parseFloat(document.getElementById('weight').value) || 0;
                const filamentPrice = parseFloat(document.getElementById('filament-price').value) || 0;
                const time = parseFloat(document.getElementById('time').value) || 0;
                const profit = parseFloat(document.getElementById('profit').value) || 0;
                const quantity = parseInt(document.getElementById('quantity').value) || 1;

                try {
                    const response = await fetch('/api/calculate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            printer: 'A1',
                            weight,
                            filament_price: filamentPrice,
                            time,
                            profit,
                            quantity
                        })
                    });

                    const result = await response.json();
                    
                    if (result.error) {
                        alert('Erro: ' + result.error);
                        return;
                    }

                    lastResult = result;
                    updateUI(result);
                    
                    // Enable copy button
                    document.getElementById('copy-btn').disabled = false;
                    
                } catch (error) {
                    alert('Erro ao calcular: ' + error.message);
                }
            }

            // Update UI with results
            function updateUI(result) {
                // Update main price display
                document.getElementById('price-display').textContent = formatCurrency(result.results.sale_price);
                
                // Update results grid
                document.getElementById('total-cost').textContent = formatCurrency(result.results.total_cost);
                document.getElementById('price-per-piece').textContent = formatCurrency(result.results.price_per_piece);
                document.getElementById('profit-amount').textContent = formatCurrency(result.results.profit_amount);
                document.getElementById('profit-percentage').textContent = result.results.profit_percentage + '%';
                
                // Update cost breakdown
                document.getElementById('cost-material').textContent = formatCurrency(result.costs.material);
                document.getElementById('cost-energy').textContent = formatCurrency(result.costs.energy);
                document.getElementById('cost-wear').textContent = formatCurrency(result.costs.wear);
                document.getElementById('cost-failure').textContent = formatCurrency(result.costs.failure);
                document.getElementById('cost-maintenance').textContent = formatCurrency(result.costs.maintenance);
                document.getElementById('cost-depreciation').textContent = formatCurrency(result.costs.depreciation);
                document.getElementById('cost-roi').textContent = formatCurrency(result.costs.roi);
                document.getElementById('cost-total-per-piece').textContent = formatCurrency(result.costs.total_per_piece);
            }

            // Copy price function
            function copyPrice() {
                if (!lastResult) return;
                
                const priceText = formatCurrency(lastResult.results.sale_price);
                navigator.clipboard.writeText(priceText).then(() => {
                    const btn = document.getElementById('copy-btn');
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '✅ Copiado!';
                    
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                    }, 2000);
                });
            }

            // Add enter key support
            document.querySelectorAll('input').forEach(input => {
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        calculate();
                    }
                });
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        data = request.get_json()
        printer = data.get('printer', 'A1')
        weight = float(data.get('weight', 0))
        filament_price = float(data.get('filament_price', 0))
        time = float(data.get('time', 0))
        profit = float(data.get('profit', 0))
        quantity = int(data.get('quantity', 1))
        
        result = calculate_costs(printer, weight, filament_price, time, profit, quantity)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Vercel entrypoint
handler = app

# Alternative entrypoints
app = app
application = app
