import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './components/ui/card';
import { Input } from './components/ui/input';
import { Select } from './components/ui/select';
import { Button } from './components/ui/button';

function App() {
  const [substance, setSubstance] = useState('');
  const [firstProperty, setFirstProperty] = useState('');
  const [firstValue, setFirstValue] = useState('');
  const [secondProperty, setSecondProperty] = useState('');
  const [secondValue, setSecondValue] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCalculate = async () => {
    if (!substance || !firstProperty || !firstValue || !secondProperty || !secondValue) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:5000/api/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          substance,
          firstProperty,
          firstValue: parseFloat(firstValue),
          secondProperty,
          secondValue: parseFloat(secondValue)
        }),
      });

      const data = await response.json();
      if (data.status === 'success') {
        setResults(data);
      } else {
        setError(data.message || 'Calculation failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to calculate properties');
    } finally {
      setLoading(false);
    }
  };

  // Filter out first property from second property options
  const getSecondPropertyOptions = () => {
    const allProperties = [
      { value: 'pressure', label: 'Pressure' },
      { value: 'temperature', label: 'Temperature' },
      { value: 'specific_volume', label: 'Specific Volume' },
      { value: 'internal_energy', label: 'Internal Energy' },
      { value: 'enthalpy', label: 'Enthalpy' },
      { value: 'entropy', label: 'Entropy' }
    ];
    return allProperties.filter(prop => prop.value !== firstProperty);
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="container mx-auto p-4">
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Thermodynamics Property Calculator</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium leading-none">
                  Substance
                </label>
                <Select 
                  value={substance} 
                  onChange={(e) => {
                    setSubstance(e.target.value);
                    setError(null);
                  }}
                >
                  <option value="">Select a substance...</option>
                  <option value="water">Water</option>
                  <option value="r134a">R134a</option>
                  <option value="ammonia">Ammonia</option>
                  <option value="co2">CO2</option>
                  <option value="propane">Propane</option>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium leading-none">
                  First Property
                </label>
                <Select 
                  value={firstProperty} 
                  onChange={(e) => {
                    setFirstProperty(e.target.value);
                    setSecondProperty('');
                    setError(null);
                  }}
                >
                  <option value="">Select property type...</option>
                  <option value="pressure">Pressure</option>
                  <option value="temperature">Temperature</option>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium leading-none">
                  First Value
                </label>
                <Input
                  type="number"
                  placeholder="Enter value..."
                  value={firstValue}
                  onChange={(e) => {
                    setFirstValue(e.target.value);
                    setError(null);
                  }}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium leading-none">
                  Second Property
                </label>
                <Select 
                  value={secondProperty}
                  onChange={(e) => {
                    setSecondProperty(e.target.value);
                    setError(null);
                  }}
                  disabled={!firstProperty}
                >
                  <option value="">Select property type...</option>
                  {getSecondPropertyOptions().map(prop => (
                    <option key={prop.value} value={prop.value}>
                      {prop.label}
                    </option>
                  ))}
                </Select>
              </div>

              {secondProperty && (
                <div className="space-y-2">
                  <label className="text-sm font-medium leading-none">
                    Second Value
                  </label>
                  <Input
                    type="number"
                    placeholder="Enter value..."
                    value={secondValue}
                    onChange={(e) => {
                      setSecondValue(e.target.value);
                      setError(null);
                    }}
                  />
                </div>
              )}

              {error && (
                <div className="text-sm text-red-500 p-2 rounded bg-red-50">
                  {error}
                </div>
              )}

              <Button 
                className="w-full"
                onClick={handleCalculate}
                disabled={loading || !substance || !firstProperty || !firstValue || !secondProperty || !secondValue}
              >
                {loading ? 'Calculating...' : 'Calculate'}
              </Button>

              {results && (
                <>
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">State Information</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p><strong>State:</strong> {results.state}</p>
                      <p><strong>Details:</strong> {results.details}</p>
                    </CardContent>
                  </Card>

                  {results.saturationProperties && (
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg">Saturation Properties</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          {Object.entries(results.saturationProperties).map(([key, value]) => (
                            <div key={key} className="flex justify-between items-center">
                              <span>{key}:</span>
                              <span className="font-mono">{value.toFixed(4)}</span>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default App;