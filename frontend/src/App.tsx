import React, { useState } from 'react'
import axios from 'axios'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [link, setLink] = useState('')
  const [linkType, setLinkType] = useState('youtube')
  const [summary, setSummary] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isError, setIsError] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const requestBody = {
      linkType,
      link
    }

    setIsLoading(true)
    setSummary('')

    try {
      const response = await axios.post('http://localhost:5000/summarize', requestBody, {
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.status == 200) {
        console.log("Response ==> ", response.data)
        setIsError(false)
        setSummary(response.data.summary)
      } else if (response.status == 400) {
        console.error("Failed to submit.")
        setIsError(true)
        setSummary(response.data.message)
      } else {
        console.error("Failed to submit.")
        setIsError(true)
        setSummary('error')
      }
    } catch (error: any) {
      console.error('Error ==> ', error.message)
      setIsError(true)
      setSummary(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className='w-screen h-screen bg-cream flex flex-col gap-4 justify-evenly'>

      {/* header */}
      <div className='w-full m-0 pl-5 h-20 flex items-center'>
        <p className='text-3xl font-cesko-regular text-golden-wheat'>essenz</p>
      </div>

      {/* main content */}
      <form onSubmit={handleSubmit} className='w-4/5 mx-auto mt-6 p-4 bg-ivory rounded-xl shadow-md'>

        <div className='flex items-center gap-4'>

          <select
            name="link-type"
            id="link-type"
            value={linkType}
            onChange={(e) => setLinkType(e.target.value)}
            className='p-4 border-gray-400 duration-300 transition-all ease-in-out rounded-md focus:outline-none focus:ring-2 focus:bg-pale-wheat/70 focus:ring-golden-wheat bg-transparent hover:bg-pale-wheat/50 text-md font-poppins-regular'
            aria-label='Choose type...'
          >
            <option value="youtube">YouTube</option>
            <option value="webpage">WebPage</option>
          </select>

          <input
            type="text"
            placeholder='Enter the link here...'
            value={link}
            onChange={(e) => setLink(e.target.value)}
            className='p-4 border-none outline-none font-poppins-regular flex-grow bg-transparent text-md focus:outline-none focus:ring-2 focus:ring-golden-wheat hover:bg-pale-wheat/50 duration-300 transition-all ease-in-out rounded-md placeholder:text-gray-600'
          />
        </div>
        <button
          type="submit"
          className="mt-4 w-full p-3 outline-none font-poppins-regular text-lg bg-pale-wheat/60 text-golden-wheat rounded-lg hover:bg-golden-wheat/70 hover:text-ivory focus:bg-golden-wheat/40 focus:ring-2 focus:ring-golden-wheat transition duration-300 ease-in-out"
        >
          Summarize
        </button>
      </form>

      <div className='w-4/5 mx-auto mt-6 p-6 mb-4 bg-ivory rounded-xl flex-grow shadow-md overflow-y-auto'>

        {isLoading ? (
          <div className="flex justify-center items-center">
            <div className="animate-spin rounded-full h-5 w-5 border-t-4 border-golden-wheat"></div>
            <p className="ml-4 text-md font-poppins-regular text-golden-wheat">Summarizing...</p>
          </div>
        ) : (
          summary && (
            <>
              <p className='text-xl font-poppins-semibold'>Summary</p>
              <p className={`text-justify font-poppins-regular text-gray-950 ${isError && 'text-red-500'}`}>{summary}</p>
            </>
          ))

          // <p className="text-center text-gray-700">{responseMessage}</p> // Display response message here
        }
      </div>

    </div>
  )
}

export default App
