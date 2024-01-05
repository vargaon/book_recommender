import { FC } from "react";
import { IBooks } from "../types";
import BookCard from "./BookCard";
import { Grid } from "@mui/material";

const BooksGrid: FC<IBooks> = ({ books }) => {
    return (
        <>
            <Grid container spacing={4} sx={{
            }}>
                {books.map((book) => (
                    <Grid item key={book.id} xs={12} sm={6} md={4} lg={3} xl={2}>
                        <BookCard book={book}></BookCard>
                    </Grid>
                ))}
            </Grid>
        </>
    )
}

export default BooksGrid;