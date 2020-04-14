import React, { Component } from 'react';
import { Container, Form, Button } from 'react-bootstrap';

import '../Style/Authenticate.css';

class Register extends Component {
    constructor(props) {
        super(props);
        this.state = {
            email: "",
            username: "",
            password: "",
        }
    }

    onChange = (e) => {
        this.setState({ [e.target.name]: e.target.value });
    }

    onSubmit = () => {
        this.props.register(this.state);
    }

    render() {
        return (
            <div className="login">
                <h1>Register</h1>
                <Form style={{ margin: "10px 10px" }}>
                    <Form.Group controlId="formBasicEmail">
                        <Form.Label>Email</Form.Label>
                        <Form.Control name='email' type="text" placeholder="Enter email" onChange={this.onChange} />
                    </Form.Group>
                    <Form.Group controlId="formBasicUsername">
                        <Form.Label>Username</Form.Label>
                        <Form.Control name='username' type="text" placeholder="Enter username" onChange={this.onChange} />
                    </Form.Group>
                    <Form.Group controlId="formBasicPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control name='password' type="password" placeholder="Password" onChange={this.onChange} />
                    </Form.Group>

                </Form>
                <Button variant="primary" onClick={this.onSubmit}>
                    Submit
                    </Button>
                <Button variant="secondary" onClick={this.props.toLogin}>
                    Already have an account?
                    </Button>
            </div>

        );
    }
}

export default Register;