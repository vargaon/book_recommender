import { Outlet } from 'react-router-dom';
import { Box } from '@mui/material';
import ActionIcons from './ActionIcons';

const Root = () => {

    return (
        <>
            <ActionIcons />
            <Box sx={{ px: 30 }}><Outlet /></Box>
        </>
    );
}

export default Root;