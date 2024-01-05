import { IconButton } from "@mui/material";
import { Link } from 'react-router-dom';
import PersonIcon from '@mui/icons-material/Person';
import HomeIcon from '@mui/icons-material/Home';

const ActionIcons = () => {

    return (
        <>
            <IconButton component={Link} to="/" sx={{
                position: "absolute",
                right: 30,
                top: 15,
                boxShadow: "0px 2px 1px -1px rgba(0,0,0,0.2), 0px 1px 1px 0px rgba(0,0,0,0.14), 0px 1px 3px 0px rgba(0,0,0,0.12)",
            }}>
                <HomeIcon sx={{
                    fontSize: 50,
                }} />
            </IconButton>
            <IconButton component={Link} to={"/user"} sx={{
                position: "absolute",
                right: 30,
                top: 95,
                boxShadow: "0px 2px 1px -1px rgba(0,0,0,0.2), 0px 1px 1px 0px rgba(0,0,0,0.14), 0px 1px 3px 0px rgba(0,0,0,0.12)",
            }}>
                <PersonIcon sx={{
                    fontSize: 50,
                }} />
            </IconButton >
        </>
    )
};

export default ActionIcons;