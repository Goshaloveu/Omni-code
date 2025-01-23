import React from "react";
import Footer from "./components/Footer";
import ShowFullItem from "./components/ShowFullItem";

let tg = window.Telegram.WebApp;

tg.expand();

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      
      ShowFullItem: false,
      Num: 0
    };

    this.btn = document.getElementsByClassName("btn");
    this.onShowItem = this.onShowItem.bind(this);
    this.componentDidMount = this.componentDidMount.bind(this);
  }

  render() {
    return (
      <div>
        {this.state.ShowFullItem && <ShowFullItem onShowItem={this.onShowItem} b={this.state.Num}/>}
        <Footer />
      </div>
    );
  }

  componentDidMount() {
    Array.from(this.btn).forEach((el) => {
      el.addEventListener("click", (event) => {
        this.onShowItem(el);
      });
    });
  };

  onShowItem(element) {
    this.setState({ ShowFullItem: !this.state.ShowFullItem , Num: element.id});
    console.log(element.id);
  }
}

export default App;
