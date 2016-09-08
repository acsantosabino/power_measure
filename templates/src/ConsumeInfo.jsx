var ConsumeInfo = React.createClass({
  loadCommentsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({current_rms: data.current_rms});
        this.setState({current_mean: data.current_mean});
        this.setState({voltage_rms: data.voltage_rms});
        this.setState({voltage_mean: data.voltage_mean});
        this.setState({power_apparent: data.power_apparent});
        this.setState({power_active: data.power_active});
        this.setState({power_factor: data.power_factor});
      }.bind(this),
      error: function(xhr, status, err) {
        this.getInitialState()
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {current_rms: [], current_mean: [], voltage_rms: [], voltage_mean: [], power_apparent: [], power_active: [], power_factor: []};
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
    setInterval(this.loadCommentsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="box consumehistory">
         <table>
                <tr>
                  <td></td>
                  <th>RMS</th>
                  <th>Média</th>
                </tr>
                <tr>
                  <th>Corrente</th>
                  <td>{this.state.current_rms}</td>
                  <td>{this.state.current_mean}</td>
                </tr>
                <tr>
                  <th>Tensão</th>
                  <td>{this.state.voltage_rms}</td>
                  <td>{this.state.voltage_mean}</td>
                </tr>
                <tr>
                  <td></td>
                  <th>Potência</th>
                  <td></td>
                </tr>
                <tr>
                  <th>Aparente</th>
                  <td>{this.state.power_apparent}</td>
                  <td></td>
                </tr>
                <tr>
                  <th>Ativa</th>
                  <td>{this.state.power_active}</td>
                  <td></td>
                </tr>
                <tr>
                  <th>Fator de Potência</th>
                  <td>{this.state.power_factor}</td>
                  <td></td>
                </tr>
         </table>
      </div>
    );
  }
});

module.exports = ConsumeInfo;  
