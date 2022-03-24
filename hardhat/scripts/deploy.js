async function main() {
    // We get the contract to deploy
    const MContract = await ethers.getContractFactory("MContract");
    const MContract = await MContract.deploy();
  
    console.log("Contract deployed to:", MContract.address);
  }
  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });