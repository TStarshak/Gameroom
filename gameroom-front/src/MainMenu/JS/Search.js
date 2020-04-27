import React, { Component } from 'react';
import '../Style/StarRating.css';
import { Container, Col, Row, Button, Form } from 'react-bootstrap';

class Search extends Component {

    
    formHandler(user,toNoti, all_players) {
        let tmp = {player: this.props.user.id}
        this.props.matching()
        // console.log(JSON.stringify(tmp))
        // fetch('/api/server/match', {
        //     method:'POST',
        //     headers: {
        //         'Content-Type' : 'application/json'
        //     },
        //     body: JSON.stringify(tmp),
        // })
        // .then(res=>res.json())
        // .then((data) => {
        //     let players_ids = data.players;
        //     players_ids.push(user.id);
        //     toNoti(players_ids);
        //     console.log(players_ids)
        //     let players = players_ids.map((value)=>{return all_players[value - 1]})
        //     console.log(players);
        //     toNoti(players);
        // });
       }
    
    render() {
        return (
            <Container>
                <Form>
                    <Form.Row>
                        <Form.Group as={Col} controlID="formGame">
                            <Form.Label>Game</Form.Label>
                            <Form.Control as={'select'} >
                                <option value='lol'>League of Legend</option>
                                <option value='pubg'>Pubg</option>
                                <option value='ow'>Overwatch</option>
                                <option value='rl'>Rocket League</option>
                                <option value='d2'>Dota 2</option>
                            </Form.Control>
                        </Form.Group>
                        {/* This can be changed into region for specific games. Will implement later */}
                        <Form.Group as={Col} controlID="formRegion">
                            <Form.Label>Region</Form.Label>
                            <Form.Control as={'select'}>
                                <option value='na'>North America</option>
                                <option value='euw'>Europe West</option>
                                <option value='eue'>Europe East</option>
                                <option value='as'>Asia</option>
                            </Form.Control>
                        </Form.Group>
                        <Form.Group as={Col} controlID="formTime">
                            <Form.Label>Play Time</Form.Label>
                            <Form.Control as={'select'}>
                                <option value='1'>1 Hour</option>
                                <option value='2'>2 Hours</option>
                                <option value='3'>3 Hours</option>
                                <option value='4'>4 Hours</option>
                                <option value='5'>5 Hours+</option>
                            </Form.Control>
                        </Form.Group>
                    </Form.Row>
                    <Row>
                        <Col>
                            <Button variant="dark" disabled>Create a lobby</Button>
                        </Col>
                        <Col>
                            <Button variant="dark" disabled>Lobby List</Button>
                        </Col>
                        <Col>
                            <Button onClick={()=>{this.formHandler(this.props.user, this.props.toNoti,this.props.all_players)}}>Join a lobby</Button>
                        </Col>
                    </Row>

                </Form>
                
            </Container>
        );
    }
}



export default Search;