import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [input, setInput] = useState('')

  useEffect(() => {
    // Fetch data from backend on component mount
    fetch('/api/hello')
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => console.error('Error:', err))
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: input })
      })
      const result = await response.json()
      console.log('Response:', result)
      setInput('')
      alert('Data sent successfully!')
    } catch (err) {
      console.error('Error:', err)
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>PyWebView + FastAPI + React</h1>
        <p>{message}</p>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter some data"
          />
          <button type="submit">Send to Backend</button>
        </form>
      </main>
    </div>
  )
}

export default App
