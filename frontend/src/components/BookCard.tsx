import { IBook } from "../types";
import { Card, Typography } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import { Link } from "@mui/material";


const BookCard = ({ book }: { book: IBook }) => {
    return (
        <Link underline="none" component={RouterLink} to={`/books/${book.id}`}>
            <Card sx={{
                display: "flex",
                flexDirection: "column",
                gap: 2,
                alignItems: "center",
                maxHeight: 350,
                height: 350,
                p: 2,
                ":hover": {
                    boxShadow: "0px 20px 30px -10px rgb(38, 57, 77)"
                }
            }}>
                <img src={book.imageUrl} alt={book.title} height={250}></img>
                <Typography variant="body1" sx={{ textAlign: "center", color: "grey" }}>
                    {book.title}
                </Typography>
            </Card>
        </Link >
    )
}

export default BookCard