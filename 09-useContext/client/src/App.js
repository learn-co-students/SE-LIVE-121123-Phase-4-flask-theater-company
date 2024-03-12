
import { Route, Switch } from 'react-router-dom'
import {createGlobalStyle} from 'styled-components'
import {useEffect, useState, useContext} from 'react'
import Home from './components/Home'
import ProductionForm from './components/ProductionForm'
import Navigation from './components/Navigation'
import ProductionDetail from './components/ProductionDetail'
import NotFound from './components/NotFound'
import Authentication from './components/Authentication'
import { UserContext } from './context/user'
import { useProduction } from './context/production'

function App() {
  // const [productions, setProductions] = useState([])
  // const [user, setUser] = useState(null)
  const { user, setUser } = useContext(UserContext)
  const { productions, setProductions } = useProduction()

  useEffect(() => {
    fetchUser()
    
  },[])

  useEffect(() => {
    fetchProductions()
  }, [user])

  const fetchProductions = () => {
    fetch('/productions')
    .then(res => {
      if (res.ok){
        res.json()
        .then(setProductions)
      }}
    )}


  const fetchUser = () => (
    fetch('/authorized')
    .then(res => {
      if(res.ok){
        res.json()
        .then(data => {
          setUser(data)
        })
      } else {
        setUser(null)
      }
    })
  )
 
  const addProduction = (production) => setProductions(current => [...current,production])
  
  const updateUser = (user) => setUser(user)
  
  if(!user) return (
    <>
      <GlobalStyle />
      <Navigation/>
      <Authentication updateUser={updateUser}/>
    </>
  )

  return (
    <>
    <GlobalStyle />
    <Navigation updateUser={updateUser}/>
      <Switch>
        <Route path='/productions/new'>
          <ProductionForm addProduction={addProduction}/>
        </Route>
        <Route path='/productions/:id'>
            <ProductionDetail />
        </Route>
        <Route exact path='/authentication'>
          <Authentication updateUser={updateUser}/>
        </Route>
        <Route exact path='/'>
          <Home />
        </Route>
        <Route>
          <NotFound />
        </Route>
      </Switch>
    </>
  )
}

export default App

const GlobalStyle = createGlobalStyle`
    body{
      background-color: black; 
      color:white;
    }
    `

