
#include "RecommendationSystem.h"

#define MIN_NUM -100000

double ranks_average(const rank_map& ranks)
{
  double sum = 0;
  for (const auto& pair: ranks)
  {
    sum += pair.second;
  }
  return sum / (double)ranks.size();
}

rank_map normalized_ranks(rank_map& ranks, double average)
{
  for (auto& pair : ranks)
  {
    pair.second -= average;
  }

  return ranks;
}

std::vector<double> operator*(const std::vector<double>& v, double c)
{
  std::vector<double> mult_vector(v.size());

  for (size_t i = 0; i < v.size(); ++i)
  {
    mult_vector[i] = c * v[i];
  }

  return mult_vector;
}

double operator*(const std::vector<double>& v1,
                 const std::vector<double>& v2)
{
  double mult = 0;

  for (size_t i = 0; i < v1.size(); ++i)
  {
    mult += (v1[i] * v2[i]);
  }

  return mult;
}

std::vector<double>& operator+=(std::vector<double>& v1,
                              const std::vector<double>& v2)
{
  std::vector<double> sum_vector(v1.size());

  for (size_t i = 0; i < v1.size(); ++i)
  {
    v1[i] += v2[i];
  }

  return v1;
}

double norm(const std::vector<double>& v)
{
  double sum = 0;

  for (const auto& elem : v)
  {
    sum += (elem * elem);
  }

  return sqrt(sum);
}

bool compare_func(const sp_movie& m1,const sp_movie& m2)
{
  return (*m1 < *m2);
}

RecommendationSystem::RecommendationSystem ()
{
  equal_func comp_func = compare_func;
  _movie_map = movie_map (comp_func);
}

sp_movie RecommendationSystem::recommend_by_content (const User &user)
{
  // step 1
  rank_map ranks = user.get_ranks();
  double average = ranks_average (ranks);
  rank_map normed_ranks = normalized_ranks (ranks, average);

  // step 2
  std::vector<double> vector_rank(_movie_map.begin()->second.size());
  for (const auto& movie : _movie_map)
  {
    std::vector<double> vec_to_add = movie.second * normed_ranks[movie.first];
    vector_rank += vec_to_add;
  }

  // step 3
  sp_movie recommended_movie;
  double max_imagination = MIN_NUM;
  for (const auto& movie : _movie_map)
  {
    if (ranks.find(movie.first) == ranks.end())  // unwatched movie
    {
      double cur_imagine = (vector_rank * movie.second)/(norm (vector_rank) *
                                                         norm (movie.second));
      if (cur_imagine > max_imagination)
      {
        max_imagination = cur_imagine;
        recommended_movie = movie.first;
      }
    }
  }

  return recommended_movie;
}

sp_movie RecommendationSystem::add_movie (const std::string &name, int year,
                                          const std::vector<double> &features)
{
  auto* new_movie = new Movie (name, year);
  sp_movie movie_to_add(new_movie);
  _movie_map.emplace(movie_to_add, features);
  return movie_to_add;
}

double RecommendationSystem::predict_movie_score (const User &user,
                                           const sp_movie &movie, int k)
{
  rank_map ranks = user.get_ranks();
  std::map<double, sp_movie, std::greater<>> total_map;
  for (const auto& ranked_movie : _movie_map)
  {
    // the user ranked the movie
    if (ranks.find(ranked_movie.first) != ranks.end())
    {
      double cur_rank = (_movie_map[movie] * ranked_movie.second) /
                        (norm(_movie_map[movie]) * norm(ranked_movie.second));
      total_map[cur_rank] = ranked_movie.first;
    }
  }
  std::map<sp_movie, double> k_map;
  int count = 0;
  for (const auto& m : total_map)
  {
    if (count >= k)
    {
      break;
    }
    ++count;
    k_map[m.second] = m.first;
  }

  double numerator = 0;
  double denominator = 0;
  for (const auto& m : k_map)
  {
    numerator += (m.second * ranks[m.first]);
    denominator += m.second;
  }
  double prediction = numerator / denominator;
  return prediction;
}

sp_movie RecommendationSystem::recommend_by_cf (const User &user, int k)
{
  rank_map ranks = user.get_ranks();
  std::map<double, sp_movie> pred_map;
  for (const auto& movie : _movie_map)
  {
    if (ranks.find(movie.first) == ranks.end())  // unwatched movie
    {
      double cur_pred = predict_movie_score (user, movie.first, k);
      pred_map[cur_pred] = movie.first;
    }
  }

  sp_movie recommended_movie = pred_map.rbegin()->second;

  return recommended_movie;
}

sp_movie RecommendationSystem::get_movie (const std::string &name,
                                          int year) const
{
  auto* movie = new Movie (name, year);
  sp_movie movie_to_find(movie);
  if (_movie_map.find (movie_to_find) == _movie_map.end())
  {
    return nullptr;
  }

  return _movie_map.find (movie_to_find)->first;
}

std::ostream& operator<< (std::ostream& os,
                          RecommendationSystem& rec_sys)
{
  for (const auto& movie_pair : rec_sys._movie_map)
  {
    os << *movie_pair.first << std::endl;
  }

  return os;
}