

// don't change those include
#include "User.h"
#include "RecommendationSystem.h"


// implement your cpp code here

User::User (const std::string& user_name, const rank_map& ranks,
            const rs_sp& rec_sys)
{
  _user_name = user_name;
  _ranks = ranks;
  _rec_sys = rec_sys;
}

const std::string &User::get_name () const
{
  return _user_name;
}

void User::add_movie_to_rs (const std::string& name, int year,
                            const std::vector<double>& features, double rate)
{
  _rec_sys->add_movie (name, year, features);
  auto* movie = new Movie (name, year);
  sp_movie new_movie(movie);
  _ranks[new_movie] = rate;
}

const rank_map &User::get_ranks () const
{
  return _ranks;
}

sp_movie User::get_recommendation_by_content () const
{
  return _rec_sys->recommend_by_content (*this);
}

sp_movie User::get_recommendation_by_cf (int k) const
{
  return _rec_sys->recommend_by_cf (*this, k);
}

double User::get_prediction_score_for_movie (const std::string &name,
                                             int year, int k) const
{
  auto* movie = new Movie (name, year);
  sp_movie movie_to_pred(movie);
  return _rec_sys->predict_movie_score (*this, movie_to_pred, k);
}

std::ostream& operator<< (std::ostream& os, User& user)
{
  os << "name: " << user._user_name << endl << *user._rec_sys << endl;
  return os;
}

