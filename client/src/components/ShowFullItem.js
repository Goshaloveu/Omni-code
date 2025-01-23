import React, { Component } from "react";
import Sortable from "./Sortable.js";

export class ShowFullItem extends Component {
  constructor(props) {
    super(props);
    
    console.log(props);
    this.close_btn = "None";
    this.componentDidMount = this.componentDidMount.bind(this);
    this.localOnShowItem = this.localOnShowItem.bind(this);
  }
  
  render() {
    return (
      <div className="full-item">
        <div>
          <button className="btn" id="close_btn">
            Закрыть
          </button>
          <Sortable b={this.props.b}/>
        </div>
      </div>
    );
  }


  localOnShowItem() {
    this.props.onShowItem(this.close_btn);
  }

  componentDidMount() {
    this.close_btn = document.querySelector("#close_btn");

    this.close_btn.addEventListener("click", this.localOnShowItem);
  }

  componentWillUnmount() {
    this.close_btn.removeEventListener("click", this.localOnShowItem);
  }
}

export default ShowFullItem;
