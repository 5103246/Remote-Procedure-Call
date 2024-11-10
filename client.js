const net = require('net');
const sever_address = '/tmp/socket_file';
const client = net.createConnection(sever_address, () => {
    console.log('connected to the server');
    const request = {
        "method": 'sort',
        "params": ['vncrA'],
        "param_types": ['str'],
        "id": 1
    };
    client.write(JSON.stringify(request));
});

client.on('data', (data) => {
    console.log('Received: ', data.toString());
    client.end()
});

client.on('end', () => {
    console.log('Disconnected from server');
});