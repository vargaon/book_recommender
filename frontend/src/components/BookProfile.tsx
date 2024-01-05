import { getBook } from "../api/BooksApi";
import { useLoaderData } from "react-router-dom";
import { IBook } from "../types";
import { Box, Typography, Rating, IconButton } from "@mui/material";
import { useState, useEffect } from "react";
import { getUserRatingOfBook, createUserRating, removeUserRating } from "../api/RatingsApi";
import { getRecommendedBooksToBook } from "../api/RecommendationApi";
import BooksGrid from "./BooksGrid";
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { CircularProgress } from "@mui/material";

export const loader = async ({ params }: any) => {
    return await getBook(params.bookId);
}

const BookProfile = ({ userId }: { userId: string }) => {
    const book = useLoaderData() as IBook;
    const [userRating, setUserRating] = useState(0);
    const [similarBooks, setSimilarBooks] = useState<IBook[]>([]);
    const [loading, setLoading] = useState(true);

    const [page, setPage] = useState(1);
    const pageSize = 6;

    const handleNextPage = () => {
        setPage(page + 1);
    };

    const handlePrevPage = () => {
        if (page > 1) setPage(page - 1);
    };

    const handleRatingChange = (rating: number | null) => {
        if (rating === null) {
            setUserRating(0);
            removeUserRating(userId, book.id);
        } else {
            setUserRating(rating);
            createUserRating(userId, book.id, rating);
        }
    }

    const fetchBookRating = async () => {
        getUserRatingOfBook(userId, book.id)
            .then(data => {
                if (data === null) setUserRating(0);
                else setUserRating(data.rating);
            })
            .catch(err => {
                console.log(err);
                setUserRating(0);
            })
    }

    useEffect(() => {
        if (userId) {
            fetchBookRating();
        }

    }, [userId]);

    useEffect(() => {
        getRecommendedBooksToBook(book.id, pageSize, (page - 1))
            .then(async data => {
                const promises = await data.map(async rec => getBook(rec.bookId));
                const values = await Promise.all(promises);
                setSimilarBooks(values);
            })
            .catch(err => {
                console.log(err);
                setSimilarBooks([]);
            })
            .finally(() => setLoading(false))
    }, [book, page])

    const content = (loading) ? <CircularProgress /> : <BooksGrid books={similarBooks} />;

    return (
        <>
            <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
                <Box sx={{ display: "flex", flexDirection: "row", gap: 2, p: 2 }}>
                    <Box><img src={book.imageUrl}></img></Box>
                    <Box sx={{ display: "flex", flexDirection: "column", gap: 1, p: 2 }}>
                        <Typography variant="h3">{book.title}</Typography>
                        <Typography variant="h6" sx={{ color: "gray" }}>{book.authors.reduce((reducer, value) => { return `${reducer}, ${value}` })}</Typography>
                        <Box>
                            {book.genres.map((g, index) => {
                                return (<Typography sx={{
                                    px: 1,
                                    mr: 1,
                                    mt: 1,
                                    borderRadius: '16px',
                                    display: 'inline-block',
                                    boxShadow: "0px 2px 1px -1px rgba(0,0,0,0.2), 0px 1px 1px 0px rgba(0,0,0,0.14), 0px 1px 3px 0px rgba(0,0,0,0.12)",
                                }} key={index}>{g}</Typography>)
                            })}
                        </Box>
                        <Typography variant="body2" sx={{
                            mt: 2,
                            textAlign: "justify",
                        }}>{book.description}</Typography>
                        <Box display={"flex"} flexDirection={"row"} visibility={(userId) ? "visible" : "hidden"} sx={{
                            mt: 1,
                        }}>
                            <Typography variant="h6" sx={{ textDecoration: "underline", mr: 1 }}>Rating</Typography>
                            <Rating name="simple-controlled" value={userRating} onChange={(_, v) => handleRatingChange(v)} size="large" />
                        </Box>
                    </Box>
                </Box >

                <Box display={"flex"} flexDirection={"row"} sx={{ p: 2 }}>
                    <IconButton type="button" aria-label="prev-page" onClick={handlePrevPage} disabled={page < 2} sx={{
                        ":hover": {
                            backgroundColor: "white"
                        }
                    }}>
                        <ArrowBackIosIcon />
                    </IconButton>
                    {content}
                    <IconButton type="button" aria-label="next-page" onClick={handleNextPage} sx={{
                        ":hover": {
                            backgroundColor: "white"
                        }
                    }}>
                        <ArrowForwardIosIcon />
                    </IconButton>
                </Box>
            </Box >

        </>
    )
}

export default BookProfile;