import {Button, Col, Container, Nav, Navbar, NavDropdown, Row} from "react-bootstrap"
import {ReactComponent as Logo} from "../../logo.svg"
import {navigate, usePath} from "hookrouter"
import {Context} from "../../Store"
import {useContext} from "react"

function Header() {
    const [state, setState] = useContext(Context)
    if (state.access_token !== "") {
        console.log(state.access_token)
        console.log(state)
        sessionStorage.setItem("name", state.name)
        sessionStorage.setItem("access_token", state.access_token)
    }

    const name = sessionStorage.getItem("name")
    const token = sessionStorage.getItem("access_token")

    let location = usePath()

    function logout() {
        setState({
            name: "",
            access_token: ""
        })
        sessionStorage.clear()
        navigate("/")
    }

    if (token && token !== "" && token !== undefined) {
        return (
            <>
                <Row>
                    <Col>
                        <Navbar bg="light" expand="lg">
                            <Container fluid>
                                <Navbar.Brand href="/home">
                                    <Logo width={"40px"} height={"40px"}/>
                                    YouTube - Scraper</Navbar.Brand>
                                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                                <Navbar.Collapse className="justify-content-end">
                                    <Nav activeKey={location.pathname} className="container-fluid">
                                        <NavDropdown title="Video" id="basic-nav-dropdown">
                                            <NavDropdown.Item href="/createvideojob">Video Scraper</NavDropdown.Item>
                                            <NavDropdown.Item href="/loadvideos">Load Videos</NavDropdown.Item>
                                        </NavDropdown>
                                        <Nav.Link href="/createcommentjob">Comment Scraper</Nav.Link>
                                        <Nav.Link href="/translator">Translator</Nav.Link>
                                        <NavDropdown title="API" id="basic-nav-dropdown">
                                            <NavDropdown.Item href="/createapi">Create API</NavDropdown.Item>
                                            <NavDropdown.Item href="/viewapis">View APIs</NavDropdown.Item>
                                        </NavDropdown>
                                        <Navbar.Text className="ms-auto">
                                            <Button  className={"headerButton"} onClick={logout}>Logout {name}</Button>
                                        </Navbar.Text>
                                    </Nav>
                                </Navbar.Collapse>
                            </Container>
                        </Navbar>
                    </Col>
                </Row>
            </>
        )
    } else {

        return (
            <>
                <Row>
                    <Col>
                        <Navbar bg="light" expand="lg">
                            <Container fluid>
                                <Navbar.Brand href="/login">
                                    <Logo width={"40px"} height={"40px"}/>
                                    YouTube - Scraper</Navbar.Brand>
                                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                                <Navbar.Collapse className="justify-content-end">
                                    <Nav activeKey={location.pathname} className="container-fluid">
                                    </Nav>
                                </Navbar.Collapse>
                            </Container>
                        </Navbar>
                    </Col>
                </Row>
            </>
        )
    }
}

export default Header

