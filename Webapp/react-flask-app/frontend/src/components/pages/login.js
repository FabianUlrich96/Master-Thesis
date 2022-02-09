import {Button, Form} from "react-bootstrap"

function Login() {
    return (
        <div className="color-overlay d-flex justify-content-center align-items-center m-lg-4">
            <Form className="rounded p-4 p-sm-3">
                <Form.Group className="mb-3">
                    <Form.Label>User</Form.Label>
                    <Form.Control type="text" placeholder="Enter username" />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter password"/>
                </Form.Group>
                <Button variant="primary" type="submit">Login</Button>
            </Form>
        </div>
    )
}

export default Login