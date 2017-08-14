var React = require('react');

var Graph = React.createClass({
  getInitialState: function() {
    return { imageStatus: null };
  },
  handleImageLoaded() {
    this.setState({ imageStatus: 'loaded' });
  },
  handleImageErrored() {
    this.setState({ imageStatus: 'failed to load' });
  }, 
  graphupdate: function() {
      var myImageElement = document.getElementById(this.props.id);
      console.log('Imgurl: ', this.props.url + '?rand=' + Math.random());
      myImageElement.src = this.props.url + '?rand=' + Math.random();
  },
  componentDidMount: function() {
    this.graphupdate();
    setInterval( this.graphupdate, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="box graph">
        <img src={this.props.url} id={this.props.id}/>
      </div>
    );
  }
});

module.exports = Graph;
