export interface IBook {
    id: string;
    title: string;
    description: string;
    imageUrl: string;
    authors: string[];
    genres: string[];
}

export interface IBooks {
    books: IBook[]
}

export interface IUserRating {
    bookId: string;
    rating: number;
}

export interface IBookRecommendation {
    bookId: string;
    score: number;
}