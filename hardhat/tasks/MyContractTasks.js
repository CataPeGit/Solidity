
task("read-number", "Reads the number")
  .addParam("contract", "The contract")
  .setAction(async (tasksArgs) => {
    const contractAddress = tasksArgs.contract
    const MContract = await ethers.getContractFactory("MContract")

    const accounts = await ethers.getSigners()
    const signer = accounts[0]
    const MContract = await new ethers.Contract(contractAddress, MContract.interface, signer)

    let result = BigInt(await MContract.getNumber()).toString()

    console.log("Stored value is: " + result);
  });

task("write-number", "Writes the number")
  .addParam("contract", "The contract")
  .addParam("value", "The value")
  .setAction(async (tasksArgs) => {
    const contractAddress = tasksArgs.contract;
    const value = tasksArgs.value;

    const MContract = await ethers.getContractFactory("MContract");

    const accounts = await ethers.getSigners();
    const signer = accounts[0];
    const MContract = await new ethers.Contract(contractAddress, MContract.interface, signer);

    let value = await MContract.setNumber(value);

    console.log("Value set: " + value);
  });

module.exports = {};