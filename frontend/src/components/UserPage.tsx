import BooksGrid from "./BooksGrid";
import { getUserRatings } from "../api/RatingsApi";
import { getBook } from "../api/BooksApi";
import { IBook } from "../types";
import { useState, useEffect } from "react";
import PersonIcon from '@mui/icons-material/Person';

import { Paper, IconButton, InputBase, Box } from "@mui/material"
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ClearIcon from '@mui/icons-material/Clear';

const UserPage = ({ userId, setUserId }: { userId: string; setUserId: (userId: string) => void }) => {

    const [books, setBooks] = useState<IBook[]>([]);
    const [page, setPage] = useState(1);

    const pageSize = 12;

    const handleNextPage = () => {
        setPage(page + 1);
    };

    const handlePrevPage = () => {
        if (page > 1) setPage(page - 1);
    };

    const handleUserChange = (userId: string) => {
        setUserId(userId);
    };

    const handleClearUser = () => {
        setUserId("");
    }

    useEffect(() => {
        getUserRatings(userId, pageSize, (page - 1) * pageSize)
            .then(async data => {
                const promises = await data.map(async rat => getBook(rat.bookId));
                const values = await Promise.all(promises);

                setBooks(values);
            })
            .catch(err => {
                console.log(err);
                setBooks([]);
            })

    }, [userId, page]);

    return (
        <Box display={"flex"} flexDirection={"column"} gap={2} p={2}>
            <Paper component="form"
                sx={{ p: '2px 4px', display: 'flex', alignItems: 'center' }}>
                <IconButton type="button" sx={{ p: '10px' }} aria-label="person" disabled={true}>
                    <PersonIcon />
                </IconButton>
                <InputBase placeholder={"User"} value={userId} sx={{ ml: 1, flex: 1 }} name="search" onChange={(e) => { handleUserChange(e.target.value) }} />
                <IconButton type="button" sx={{ p: '10px' }} aria-label="clear" onClick={handleClearUser} disabled={userId ? false : true}>
                    <ClearIcon />
                </IconButton>
                <IconButton type="button" sx={{ p: '10px' }} aria-label="prev-page" onClick={handlePrevPage} disabled={page < 2}>
                    <ArrowBackIosIcon />
                </IconButton>
                <IconButton type="button" sx={{ p: '10px' }} aria-label="next-page" onClick={handleNextPage} disabled={books.length < pageSize}>
                    <ArrowForwardIosIcon />
                </IconButton>
            </Paper>
            <BooksGrid books={books} />
        </Box >
    )
};

export default UserPage;

