import React, { Component } from 'react';

import ProfileIcon from './ProfileIcon';
import '../Style/PlayerRate.css';
import { Row, Col, Button } from 'react-bootstrap';
import Popup from "reactjs-popup";

class PlayerRate extends Component {
    constructor(props) {
        super(props);
        this.state = {choices: [0, 0, 0]};
        this.ClickHandler = this.ClickHandler.bind(this);
    }

    ClickHandler(index, choice){
        let tmp = this.state.choices;
        tmp[index] = choice;
        this.setState({choices: tmp});
        this.props.update(tmp);
    }
    render() {
        let words = [['Skilled','Bad'],['Friendly','Toxic'],['Funny','Boring']];
        let popupElements = this.state.choices.map((choice,index) => {
            let but1;
            let but2;
            if(choice == 1){
                but1 = <Button onClick={()=>{this.ClickHandler(index,0)}}>{words[index][0]}</Button>;
            }
            else {
                but1 = <Button onClick={()=>{this.ClickHandler(index,1)}} variant='light'>{words[index][0]}</Button>;
            }
            if(choice == 2){
                but2 = <Button onClick={()=>{this.ClickHandler(index,0)}} variant='danger'>{words[index][1]}</Button>;
            }
            else {
                but2 = <Button onClick={()=>{this.ClickHandler(index,2)}} variant='light'>{words[index][1]}</Button>;
            }
            return <Row>
                <Col>
                    {but1}
                    {but2}
                </Col>
            </Row>
        });
    
        return (
            <div className="PlayerRate">
                <ProfileIcon></ProfileIcon>
                <h1>{this.props.player.name}</h1>
                <Popup trigger={<Button variant='info'>Rate</Button>} position='bottom center'>
                    {popupElements}

                </Popup>

                {/* <Popup trigger={<Button className="arrow"></Button>} position='bottom center'>
                    <Row>
                        <Col><Button>Skilled</Button></Col>
                        <Col><Button>Friendly</Button></Col>
                        <Col><Button>Funny</Button></Col>
                    </Row>
                    
                </Popup>

                <Popup trigger={<Button className="arrow rotate" variant='danger'></Button>} position='bottom center'>
                    <Row>
                        <Col><Button variant="danger">Bad</Button></Col>
                        <Col><Button variant="danger">Toxic</Button></Col>
                        <Col><Button variant="danger">Boring</Button></Col>
                    </Row>
                </Popup> */}
            </div>
        );
    }
}

export default PlayerRate;