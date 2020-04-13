import React, {Component} from 'react';
import {Container, Col, Row,Button} from 'react-bootstrap';
import '../Style/Rating.css';
import PlayerRate from './PlayerRate'
class Rating extends Component{
    constructor(props){
        super(props);
        this.state = {rating: props.players.map((player)=>{return [0,0,0]})};
        this.updateState = this.updateState.bind(this);
    }

    updateState(index,state){
        let tmp = this.state.rating;
        tmp[index] = state;
        this.setState({rating:tmp});
        console.log(this.state);
    }

    render(){
        
        let items = this.props.players.map((player,index)=>{
            return <Col><PlayerRate player={player} update={(ratingState)=>{this.updateState(index,ratingState)}} ></PlayerRate></Col>;
        })

        return (
            <div className="Rating">              
                    <Row>
                        {items}
                    </Row>
                    <Row>
                            <Button className="finish" onClick={this.props.toMainMenu}>
                                Finish
                            </Button>
                    </Row>
            </div>
        );
    }
}

export default Rating;