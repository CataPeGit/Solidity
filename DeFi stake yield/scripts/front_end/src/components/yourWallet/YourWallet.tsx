// this component deals with getting the wallet
// that is the different ballances of the tokens we own

import { Token } from "../Main"
import React, { useState } from "react"
import { Box, makeStyles} from "@material-ui/core"
import {TabContext, TabList, TabPanel} from "@material-ui/lab" 
import { Tab } from "@material-ui/core"
import { WalletBalance } from "./WalletBalance"
import { StakeForm } from "./StakeForm"


interface YourWalletProps {
    supportedTokens: Array<Token>
}

const useStyles = makeStyles((theme) => ({
    tabContent: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: theme.spacing(4)
    },
    box: {
        backgroundColor: "white",
        borderRadius: "25px"
    },
    header: {
        color: "white"
    }
}))

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {

    // we will use a State Hook in order to select tokens
    // selectedTokenIndex --> the token we are on
    // setSelectedTokenIndex --> update selectedTokenIndex
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)

    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue))
    }

    const classes = useStyles()

    return(
        <Box>
            <h1 className={classes.header}> Your Wallet! </h1>
            
            <Box className= {classes.box}>
                <TabContext value={selectedTokenIndex.toString()}>
                    <TabList onChange={handleChange} aria-label="stake form tabs">
                        {supportedTokens.map((token, index) => {
                            return (
                                <Tab label={token.name}
                                     value={index.toString()}
                                     key={index} 
                                />
                            )
                        })}
                    </TabList>

                    {supportedTokens.map((token, index) => {
                        return (
                            <TabPanel value={index.toString()}
                                      key={index}>
                                <div className={classes.tabContent}>
                                    <WalletBalance token={supportedTokens[selectedTokenIndex]} />
                                    <StakeForm token={supportedTokens[selectedTokenIndex]} />
                                </div>
                            </TabPanel>
                        )
                    })}

                </TabContext>
            </Box>

        </Box>
    )

}