# Student Lease

## Overview

Student Lease is a comprehensive platform designed specifically for students dealing with housing transitions. The application streamlines the process of finding sublets, selling personal belongings, and connecting with potential roommates. This project aims to enhance the overall student housing experience by providing a one-stop solution for housing needs, community building, and item management.

## Motivation

Students face unique challenges in housing transitions due to frequent relocations, financial constraints, lack of centralized services, and the need for community and networking. Student Lease addresses these needs by offering a platform tailored to the student lifestyle, providing tools for managing temporary housing, communication, and selling belongings.

## Problem Statement

Student Lease allows students to:
- Post and manage sublet listings
- Explore housing options
- Communicate with peers via an integrated chat system
- Sell personal belongings like furniture and textbooks

This platform centralizes all these functionalities to simplify student housing transitions.

## Existing Solutions

- **Zillow**: Serves a broader real estate market but lacks the student-specific focus.
- **Roomster**: Focuses on shared housing and roommate matching but does not address the sale of personal belongings or the unique needs of students.

## Architecture

### User Layer
- **Signup/Login**: Secure authentication using .edu email addresses.
- **Feed**: Personalized recommendations based on user activity.
- **Search & Filters**: Search for sublets with various filters.
- **Post Listing**: Post properties for sublease with detailed information.
- **Chat**: Integrated chat feature for user communication.

### API Layer
- **REST API**: Handles regular tasks such as creating listings and populating feeds.
- **WebSocket API**: Manages real-time chat functionalities.

### Data Layer
- **DynamoDB**: Used for storing chat messages, user data, marketplace postings, and sublet listings.
- **SQS (Simple Queue Service)**: Used to store click streams. When a user opens any listing, a Lambda function saves the user_id and listing_id in the SQS. An EventBridge Lambda trigger reads data from SQS and updates the timeVisited attribute in Elasticsearch, indicating the number of times an item has been viewed overall. Additionally, the listing_id is added to the DynamoDB against the user_id to store the last visited item list, which defaults to 10.

  - **Importance of SQS**
Using SQS allows us to focus on critical functions, reducing latency and handling non-critical functions like updating the timeVisited count asynchronously. This ensures that the application remains responsive and can handle high loads without performance degradation.
- **Elasticsearch**: Elasticsearch is used in our system to manage and search sublet listings efficiently. It provides the following functionalities:
  - **Full-Text Search:** Allows users to perform complex searches quickly and accurately.
  - **Recommendation:** We used OpenSearch service to store our elastic search data with embeddings for recommendation.
  - **Scalability:** Manages large volumes of data and high query loads with ease.
### Logical Layer
- **Recommendation Engine**: Utilizes content-based filtering to suggest compatible roommates based on detailed listing information.

## Future Work

1. **Enhanced Chat Platform**: Support for group conversations and caching for faster message retrieval.
2. **Adaptive Recommendation Engine**: Personalized suggestions based on user behavior.
3. **Price Detection**: Estimate property prices based on various factors.
4. **Sublet Information Aggregator**: Central hub for sublet information from various sources.
5. **Integration with Service Providers**: Enable booking of moving services directly through the platform.

## Results

Our project successfully created a recommendation system, chat functionality, and a platform for managing sublet postings and personal item sales. The recommendation system provided robust and accurate suggestions for users.

## Postman Collection

The repository includes a Postman collection `Cloud_computing.postman_collection.json` at the root level. This collection can be used to check how the Elasticsearch index is created and how the recommendation system utilizes embeddings. 

To use the Postman collection:
1. Open Postman.
2. Import the `Cloud_computing.postman_collection.json` file.
3. Follow the provided requests to understand and test the API endpoints related to Elasticsearch and the recommendation system.

## References

1. [AWS Documentation](https://docs.aws.amazon.com/)
2. [Building a Full-Stack Chat Application with AWS and Next.js](https://aws.amazon.com/blogs/mobile/building-a-full-stack-chat-application-with-aws-and-nextjs/)
3. [React Documentation](https://legacy.reactjs.org/docs/getting-started.html)
4. [Embedding Similar Home Recommendations](https://www.zillow.com/tech/embedding-similar-home-recommendation/)
5. [Real-Time Recommendations](https://eugeneyan.com/writing/real-time-recommendations/)

## Architecture Diagrams

![image](https://github.com/moinkhan3012/Student-Lease/assets/35172739/a48c0eef-2cc3-4504-84a5-fb5c24b19aa8)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Developed by:
- Aravindsrinivas Krishnamoorthy (ak11115@nyu.edu)
- Priyangshu Pal (pp2833@nyu.edu)
- Vir Jhangiani (vrj2006@nyu.edu)
- Moin Khan (mk8793@nyu.edu)
