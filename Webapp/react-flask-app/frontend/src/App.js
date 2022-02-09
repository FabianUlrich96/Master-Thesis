import './App.css'
import {useRoutes} from 'hookrouter'
import Routes from './router'
import Header from "./components/nav/Header"
import {Container} from "react-bootstrap"

function App() {
    return (
        <>
            <Container fluid>
                <Header/>
                {useRoutes(Routes)}
            </Container>
        </>
    )
}

export default App