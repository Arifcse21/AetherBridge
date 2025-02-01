const { ApolloServer } = require('@apollo/server');
const { ApolloGateway, IntrospectAndCompose } = require('@apollo/gateway');
const { startStandaloneServer } = require('@apollo/server/standalone');

const RETRY_DELAY = 5000; // 5 seconds
let serverStarted = false;

async function testSubgraphConnection(name, url) {
  try {
    const gateway = new ApolloGateway({
      supergraphSdl: new IntrospectAndCompose({
        subgraphs: [{ name, url }],
      }),
    });
    await gateway.load();
    return true;
  } catch (error) {
    console.log(`Failed to connect to ${name} service: ${error.message}`);
    return false;
  }
}

async function startServer(gateway) {
  if (serverStarted) {
    return;
  }

  try {
    const server = new ApolloServer({
      gateway,
      subscriptions: false,
    });

    const { url } = await startStandaloneServer(server, {
      listen: { port: 4000 }
    });

    console.log('\n🚀 Gateway ready at', url);
    serverStarted = true;
    return true;
  } catch (error) {
    if (error.code === 'EADDRINUSE') {
      console.log('\n⚠️  Port 4000 is already in use - Gateway is running on existing port');
      serverStarted = true;
      return true;
    }
    console.log(`Failed to start server: ${error.message}`);
    return false;
  }
}

async function waitForServices() {
  const subgraphs = [
    // { name: 'users', url: process.env.USER_SERVICE_URL },
    // { name: 'tasks', url: process.env.TASK_SERVICE_URL },
    { name: 'users', url: 'http://127.0.0.1:8000/graphql/' },
    { name: 'tasks', url: 'http://127.0.0.1:8001/graphql/' },
  ];

  const availableSubgraphs = [];
  let attempt = 1;
  
  while (true) {
    console.log(`\nAttempt ${attempt} to connect to services...`);
    
    // Test each subgraph that hasn't been successfully connected yet
    for (const subgraph of subgraphs) {
      if (!availableSubgraphs.some(s => s.name === subgraph.name)) {
        console.log(`Testing ${subgraph.name} service at ${subgraph.url}`);
        const isAvailable = await testSubgraphConnection(subgraph.name, subgraph.url);
        
        if (isAvailable) {
          console.log(`✅ Successfully connected to ${subgraph.name} service`);
          availableSubgraphs.push(subgraph);
        } else {
          console.log(`❌ Attempt ${attempt} failed for ${subgraph.name} service`);
        }
      }
    }

    // If we have at least one subgraph available, proceed with gateway creation
    if (availableSubgraphs.length > 0) {
      const gateway = new ApolloGateway({
        supergraphSdl: new IntrospectAndCompose({
          subgraphs: availableSubgraphs,
        }),
        pollIntervalInMs: 5000,
      });

      const serverStarted = await startServer(gateway);
      
      if (serverStarted) {
        console.log('\nAvailable services:');
        availableSubgraphs.forEach(s => console.log(`- ${s.name}`));
        
        if (availableSubgraphs.length < subgraphs.length) {
          console.log('\nUnavailable services:');
          subgraphs
            .filter(s => !availableSubgraphs.some(a => a.name === s.name))
            .forEach(s => console.log(`- ${s.name}`));
            
          // Continue retrying if some services are still unavailable
          await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
          attempt++;
          continue;
        }
        return;
      }
    }
    
    await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
    attempt++;
  }
}

waitForServices().catch(error => {
  console.error('Gateway initialization failed:', error);
  // Don't exit the process on error, let it keep retrying
  console.log('Continuing to retry...');
});