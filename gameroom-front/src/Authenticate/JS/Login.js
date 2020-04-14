import React, { Component } from 'react';
import { Container, Form, Button } from 'react-bootstrap';

import '../Style/Authenticate.css';
class Login extends Component {
    constructor(props){
        super(props);
        this.state = {
            username: '',
            password: '',
        };
    }

    onChange = (e) => {
        this.setState({[e.target.name]: e.target.value});
    }

    onSubmit = () => {
        this.props.login(this.state)
    }

    render() {
        return (
            <div className="login">
                <h1>Sign in</h1>
                <Form style={{margin: "10px 10px"}}>
                    <Form.Group controlId="formBasicUsername">
                        <Form.Label>Username</Form.Label>
                        <Form.Control name='username' type="text" placeholder="Enter username" onChange={this.onChange} />
                    </Form.Group>
                    <Form.Group controlId="formBasicPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control name='password' type="password" placeholder="Password" onChange={this.onChange}/>
                    </Form.Group>
                    
                </Form>
                <Button variant="primary" onClick={this.onSubmit}>
                        Submit
                    </Button>
                    <Button variant="secondary" onClick={()=>{this.props.toRegister(false)}}>
                        Register
                    </Button>
            </div>

        );
    }
}

export default Login;